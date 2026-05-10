# engine/anomaly_detector.py
"""
NAR8 AI — Anomaly Detection Engine

Uses three statistical methods to identify unusual sales patterns:
  1. Z-Score Analysis
  2. IQR (Interquartile Range) Analysis
  3. Rolling Average Percentage Deviation

Consensus rule: An anomaly is flagged only when >=2 of 3 methods agree.
This reduces false positives while maintaining sensitivity.
"""
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from config.settings import Config


# ─────────────────────────────────────────────────────────────────────
# Data Classes
# Dataclasses are Python's clean way to define structured data objects.
# They auto-generate __init__, __repr__, and other methods.
# ─────────────────────────────────────────────────────────────────────

@dataclass
class Anomaly:
    """Represents a single detected sales anomaly."""
    week_date:        str    # "2025-04-07"
    category:         str    # "Electronics"
    region:           str    # "North"
    metric:           str    # "Sales Amount"
    actual_value:     float  # $208,750
    expected_value:   float  # $85,200 (8-week rolling average)
    deviation_pct:    float  # +144.9 (percent)
    severity:         str    # "HIGH", "MEDIUM", or "LOW"
    direction:        str    # "SPIKE" or "DROP"
    z_score:          float  # 4.21
    methods_triggered: int   # How many of 3 methods flagged this
    description:      str    # Human-readable one-liner


@dataclass
class AnomalyReport:
    """
    The complete output of one analysis run.
    Contains summary statistics and all detected anomalies.
    Passed to the LLM narrator and slide builder.
    """
    # Metadata
    analysis_datetime:     str
    week_analyzed:         str
    data_source:           str   # "mock" or "powerbi"

    # Anomaly findings
    total_anomalies:       int
    high_severity_count:   int
    medium_severity_count: int
    low_severity_count:    int
    anomalies:             List[Anomaly]

    # Week performance
    overall_week_sales:    float
    previous_week_sales:   float
    wow_change_pct:        float   # Week-over-week % change
    wow_direction:         str     # "UP", "DOWN", or "FLAT"

    # Segment highlights
    top_segment:           Dict    # {"name": "...", "sales": ..., "vs_avg_pct": ...}
    bottom_segment:        Dict    # same structure

    # Statistical context
    baseline_weeks_used:   int
    total_segments_checked: int
    avg_weekly_sales:      float   # Historical average total weekly sales
    categories:            List[str]
    regions:               List[str]


# ─────────────────────────────────────────────────────────────────────
# Detector Class
# ─────────────────────────────────────────────────────────────────────

class AnomalyDetector:
    """
    Analyzes a weekly sales DataFrame and produces an AnomalyReport.

    Usage:
        detector = AnomalyDetector()
        report = detector.detect(df)
    """

    def __init__(
        self,
        z_threshold: float = None,
        pct_threshold: float = None,
        lookback_weeks: int = None,
    ):
        self.z_threshold = z_threshold or Config.Z_SCORE_THRESHOLD
        self.pct_threshold = pct_threshold or Config.PCT_CHANGE_THRESHOLD
        self.lookback_weeks = lookback_weeks or Config.LOOKBACK_WEEKS

    # ── Private Helper Methods ────────────────────────────────────────

    def _z_score(self, series: pd.Series, value: float) -> float:
        """Calculates Z-score of a value against a historical series."""
        std = series.std()
        if std == 0 or pd.isna(std):
            return 0.0
        return float((value - series.mean()) / std)

    def _iqr_check(self, series: pd.Series, value: float) -> bool:
        """Returns True if value falls outside the IQR fence."""
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        return float(value) < float(lower) or float(value) > float(upper)

    def _pct_deviation(self, series: pd.Series, value: float) -> float:
        """Returns % deviation of value from series mean. Range: -1.0 to +inf."""
        mean = series.mean()
        if mean == 0 or pd.isna(mean):
            return 0.0
        return (value - mean) / mean

    def _classify_severity(self, deviation_pct: float) -> str:
        """Classifies anomaly severity based on absolute deviation percentage."""
        abs_dev = abs(deviation_pct)
        if abs_dev >= 0.60:
            return "HIGH"
        elif abs_dev >= 0.30:
            return "MEDIUM"
        else:
            return "LOW"

    def _build_description(
        self,
        category: str, region: str,
        direction: str, deviation_pct: float,
        actual: float, expected: float,
        z: float
    ) -> str:
        """Generates a concise, human-readable description of the anomaly."""
        return (
            f"{category} – {region}: Sales {direction} of "
            f"{abs(deviation_pct) * 100:.1f}% vs. {self.lookback_weeks}-week average. "
            f"Actual: ${actual:,.0f} | Expected: ~${expected:,.0f} | Z-Score: {z:.2f}"
        )

    # ── Main Detection Method ─────────────────────────────────────────

    def detect(self, df: pd.DataFrame) -> AnomalyReport:
        """
        Runs anomaly detection on the most recent week of data.

        Process:
          1. Separates current week from historical baseline
          2. For each category × region combination:
             a. Gets historical sales for that segment
             b. Applies all 3 detection methods
             c. Flags if >=2 methods agree
          3. Classifies severity and direction
          4. Compiles summary statistics
          5. Returns a complete AnomalyReport

        Args:
            df: Full historical DataFrame from PowerBIConnector

        Returns:
            AnomalyReport dataclass with all findings
        """
        df = df.sort_values("week_start_date").copy()
        all_weeks = sorted(df["week_start_date"].unique())

        if len(all_weeks) < Config.MIN_WEEKS_FOR_DETECTION:
            raise ValueError(
                f"Need at least {Config.MIN_WEEKS_FOR_DETECTION} weeks of data. "
                f"Got {len(all_weeks)}."
            )

        # ── Split data ────────────────────────────────────────────────
        current_week_date = all_weeks[-1]
        prev_week_date = all_weeks[-2]

        current_df = df[df["week_start_date"] == current_week_date].copy()
        prev_df = df[df["week_start_date"] == prev_week_date].copy()

        # Historical baseline: last N weeks, excluding current
        baseline_weeks = all_weeks[-(self.lookback_weeks + 1):-1]
        baseline_df = df[df["week_start_date"].isin(baseline_weeks)].copy()

        # ── Detect anomalies per segment ──────────────────────────────
        anomalies: List[Anomaly] = []
        segments_checked = 0

        for _, row in current_df.iterrows():
            cat = row["category"]
            reg = row["region"]
            current_sales = float(row["sales_amount"])
            segments_checked += 1

            # Historical sales for this exact segment
            hist = baseline_df[
                (baseline_df["category"] == cat) &
                (baseline_df["region"] == reg)
            ]["sales_amount"].astype(float)

            if len(hist) < 3:
                continue  # Not enough history to detect meaningfully

            # ── Apply three methods ──────────────────────────────────
            z = self._z_score(hist, current_sales)
            iqr_flagged = self._iqr_check(hist, current_sales)
            pct_dev = self._pct_deviation(hist, current_sales)

            z_flagged = abs(z) >= self.z_threshold
            pct_flagged = abs(pct_dev) >= self.pct_threshold
            methods_triggered = sum([z_flagged, pct_flagged, iqr_flagged])

            # ── Consensus rule: need >=2 methods to agree ─────────────
            if methods_triggered < 2:
                continue

            direction = "SPIKE" if pct_dev > 0 else "DROP"
            severity = self._classify_severity(pct_dev)
            expected = float(hist.mean())

            anomalies.append(Anomaly(
                week_date=str(current_week_date.date()),
                category=cat,
                region=reg,
                metric="Sales Amount",
                actual_value=round(current_sales, 2),
                expected_value=round(expected, 2),
                deviation_pct=round(pct_dev * 100, 2),
                severity=severity,
                direction=direction,
                z_score=round(z, 3),
                methods_triggered=methods_triggered,
                description=self._build_description(
                    cat, reg, direction, pct_dev,
                    current_sales, expected, z
                ),
            ))

        # ── Sort by severity then deviation magnitude ─────────────────
        severity_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        anomalies.sort(
            key=lambda a: (severity_rank[a.severity], -abs(a.deviation_pct))
        )

        # ── Summary stats ─────────────────────────────────────────────
        total_current = float(current_df["sales_amount"].sum())
        total_prev = float(prev_df["sales_amount"].sum())
        wow_change = (
            ((total_current - total_prev) / total_prev * 100)
            if total_prev > 0 else 0.0
        )
        wow_direction = (
            "UP" if wow_change > 1
            else "DOWN" if wow_change < -1
            else "FLAT"
        )

        # Best and worst segment this week
        current_df = current_df.copy()
        current_df["segment"] = current_df["category"] + " – " + current_df["region"]

        best_row = current_df.loc[current_df["sales_amount"].idxmax()]
        worst_row = current_df.loc[current_df["sales_amount"].idxmin()]

        def segment_vs_avg(seg_df_row, baseline):
            cat, reg = seg_df_row["category"], seg_df_row["region"]
            hist_avg = baseline_df[
                (baseline_df["category"] == cat) &
                (baseline_df["region"] == reg)
            ]["sales_amount"].mean()
            if hist_avg == 0 or pd.isna(hist_avg):
                return 0.0
            return ((seg_df_row["sales_amount"] - hist_avg) / hist_avg) * 100

        hist_weekly_totals = (
            baseline_df.groupby("week_start_date")["sales_amount"].sum()
        )

        return AnomalyReport(
            analysis_datetime=datetime.now().strftime("%Y-%m-%d %H:%M"),
            week_analyzed=str(current_week_date.date()),
            data_source="mock" if Config.USE_MOCK_DATA else "powerbi",
            total_anomalies=len(anomalies),
            high_severity_count=sum(1 for a in anomalies if a.severity == "HIGH"),
            medium_severity_count=sum(1 for a in anomalies if a.severity == "MEDIUM"),
            low_severity_count=sum(1 for a in anomalies if a.severity == "LOW"),
            anomalies=anomalies,
            overall_week_sales=round(total_current, 2),
            previous_week_sales=round(total_prev, 2),
            wow_change_pct=round(wow_change, 2),
            wow_direction=wow_direction,
            top_segment={
                "name": best_row["segment"],
                "sales": round(float(best_row["sales_amount"]), 2),
                "vs_avg_pct": round(segment_vs_avg(best_row, baseline_df), 1),
            },
            bottom_segment={
                "name": worst_row["segment"],
                "sales": round(float(worst_row["sales_amount"]), 2),
                "vs_avg_pct": round(segment_vs_avg(worst_row, baseline_df), 1),
            },
            baseline_weeks_used=len(baseline_weeks),
            total_segments_checked=segments_checked,
            avg_weekly_sales=round(float(hist_weekly_totals.mean()), 2),
            categories=list(df["category"].unique()),
            regions=list(df["region"].unique()),
        )
