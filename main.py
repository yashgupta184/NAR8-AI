# main.py
"""
NAR8 AI — Pipeline Orchestrator

Runs the complete NAR8 AI pipeline from the command line.
This is also imported by the Streamlit dashboard to power the UI.

Usage:
    python main.py                    # Run with defaults
    python main.py --weeks 10         # Use 10 weeks of data
    python main.py --output my_dir    # Custom output directory

Pipeline stages:
    [1] Data Fetch       -> PowerBIConnector
    [2] Anomaly Detection -> AnomalyDetector
    [3] Narrative Gen    -> LLMNarrator
    [4] Deck Build       -> SlideBuilder + ChartGenerator
"""
import argparse
import time
import os
from config.settings import Config
from data.powerbi_connector import PowerBIConnector
from engine.anomaly_detector import AnomalyDetector
from engine.llm_narrator import LLMNarrator
from output.slide_builder import build_deck


def run_pipeline(
    weeks: int = None,
    output_dir: str = None,
    z_threshold: float = None,
    pct_threshold: float = None,
    lookback_weeks: int = None,
    verbose: bool = True,
) -> dict:
    """
    Executes the full NAR8 AI pipeline.

    This function is the single entry point for both the CLI (main.py)
    and the Streamlit UI (ui/dashboard.py). It returns a result dict
    containing everything the UI needs to display.

    Args:
        weeks:         Number of weeks of data to fetch
        output_dir:    Where to save the slide deck
        z_threshold:   Z-score threshold for anomaly detection
        pct_threshold: % change threshold for anomaly detection
        lookback_weeks: How many weeks to use as baseline
        verbose:       Print progress messages

    Returns:
        {
            "success":    bool,
            "df":         DataFrame,
            "report":     AnomalyReport,
            "narrative":  dict,
            "deck_path":  str,
            "duration_s": float,
            "error":      str or None
        }
    """
    start_time = time.time()
    result = {
        "success": False,
        "df": None,
        "report": None,
        "narrative": None,
        "deck_path": None,
        "duration_s": 0.0,
        "error": None,
    }

    def log(msg):
        if verbose:
            print(msg)

    try:
        # -- Validate config -------------------------------------------
        warnings = Config.validate()
        for w in warnings:
            log(f"[WARNING] {w}")

        log("\n" + "=" * 62)
        log("  NAR8 AI — Automated Data Storytelling Pipeline")
        log("=" * 62)

        # -- Stage 1: Fetch Data ---------------------------------------
        log("\n[1/4] Fetching sales data...")
        connector = PowerBIConnector()
        df = connector.fetch_weekly_sales(weeks=weeks or Config.WEEKS_OF_DATA)
        result["df"] = df
        log(f"      [SUCCESS] {len(df)} rows | {df['week_start_date'].nunique()} weeks")
        log(f"        Categories: {', '.join(df['category'].unique())}")
        log(f"        Regions:    {', '.join(df['region'].unique())}")

        # -- Stage 2: Detect Anomalies ---------------------------------
        log("\n[2/4] Running anomaly detection engine...")
        detector = AnomalyDetector(
            z_threshold=z_threshold or Config.Z_SCORE_THRESHOLD,
            pct_threshold=pct_threshold or Config.PCT_CHANGE_THRESHOLD,
            lookback_weeks=lookback_weeks or Config.LOOKBACK_WEEKS,
        )
        report = detector.detect(df)
        result["report"] = report
        log(f"      [SUCCESS] Week: {report.week_analyzed}")
        log(f"        Anomalies: {report.total_anomalies} total "
            f"({report.high_severity_count} HIGH, "
            f"{report.medium_severity_count} MEDIUM, "
            f"{report.low_severity_count} LOW)")
        log(f"        WoW Change: {report.wow_change_pct:+.1f}%")
        if report.anomalies:
            log(f"        Top Anomaly: {report.anomalies[0].description[:80]}...")

        # -- Stage 3: Generate Narrative -------------------------------
        log("\n[3/4] Generating AI narrative...")
        narrator = LLMNarrator()
        narrative = narrator.generate_narrative(report)
        result["narrative"] = narrative
        headline = narrative.get("executive_summary", {}).get("headline", "N/A")
        log(f"      [SUCCESS] Headline: \"{headline}\"")

        # -- Stage 4: Build Slide Deck ---------------------------------
        log("\n[4/4] Building PowerPoint slide deck...")
        save_dir = output_dir or Config.OUTPUT_DIR
        deck_path = build_deck(narrative, report, df, save_dir)
        result["deck_path"] = deck_path

        # -- Done ------------------------------------------------------
        duration = round(time.time() - start_time, 1)
        result["duration_s"] = duration
        result["success"] = True

        log(f"\n{'=' * 62}")
        log(f"  [SUCCESS] NAR8 AI pipeline complete in {duration}s")
        log(f"  Deck: {deck_path}")
        log(f"{'=' * 62}\n")

    except Exception as e:
        result["error"] = str(e)
        result["duration_s"] = round(time.time() - start_time, 1)
        log(f"\n[ERROR] Pipeline failed: {e}")
        import traceback
        traceback.print_exc()

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NAR8 AI — Run the analysis pipeline")
    parser.add_argument("--weeks", type=int, default=None, help="Number of weeks to analyze")
    parser.add_argument("--output", type=str, default=None, help="Output directory for slides")
    parser.add_argument("--z-threshold", type=float, default=None)
    parser.add_argument("--pct-threshold", type=float, default=None)
    parser.add_argument("--lookback", type=int, default=None)
    args = parser.parse_args()

    result = run_pipeline(
        weeks=args.weeks,
        output_dir=args.output,
        z_threshold=args.z_threshold,
        pct_threshold=args.pct_threshold,
        lookback_weeks=args.lookback,
    )

    if not result["success"]:
        exit(1)
