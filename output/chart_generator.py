# output/chart_generator.py
"""
NAR8 AI — Chart Generator

Creates three Matplotlib charts as PNG files:
  1. Weekly sales trend line with rolling average
  2. Category sales comparison (this week vs. historical avg)
  3. Category × Region deviation heatmap

All charts use the NAR8 AI brand color palette and consistent styling.
Output PNGs are saved to output/slides/charts/ and their paths returned
to the slide builder for embedding.
"""
import os
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend — no display window needed
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from config.settings import Config
from engine.anomaly_detector import AnomalyReport


# ── Brand Colors for Matplotlib ───────────────────────────────────────
# Convert hex to matplotlib-compatible format
C = {
    "navy":       "#1E3A5F",
    "blue":       "#2E86AB",
    "green":      "#27AE60",
    "red":        "#E74C3C",
    "orange":     "#F39C12",
    "background": "#F8FAFC",
    "grid":       "#E2E8F0",
    "text":       "#1A1A2E",
    "muted":      "#95A5A6",
    "light_blue": "#EBF5FB",
}

# Global matplotlib style settings
plt.rcParams.update({
    "font.family":        "DejaVu Sans",
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.grid":          True,
    "grid.alpha":         0.5,
    "grid.color":         C["grid"],
    "axes.facecolor":     C["background"],
    "figure.facecolor":   C["background"],
    "axes.labelcolor":    C["text"],
    "xtick.color":        C["text"],
    "ytick.color":        C["text"],
    "text.color":         C["text"],
})


def _ensure_dir(path: str) -> None:
    """Creates directory if it does not already exist."""
    os.makedirs(path, exist_ok=True)


# ── Chart 1: Weekly Trend Line ────────────────────────────────────────

def create_trend_chart(df: pd.DataFrame, output_dir: str) -> str:
    """
    Line chart showing 13 weeks of total sales with rolling average.

    Visual features:
      - Clean line with circular markers
      - Dashed rolling average overlay
      - Shaded region highlighting the current (most recent) week
      - Y-axis in thousands ($K) for readability

    Returns: file path to saved PNG
    """
    _ensure_dir(output_dir)

    # Aggregate to weekly totals
    weekly = (
        df.groupby("week_start_date")["sales_amount"]
        .sum()
        .reset_index()
        .sort_values("week_start_date")
    )
    weekly["sales_k"] = weekly["sales_amount"] / 1000
    weekly["rolling_avg"] = weekly["sales_k"].rolling(4, min_periods=1).mean()
    n = len(weekly)
    x = range(n)

    fig, ax = plt.subplots(figsize=(10, 4.5))

    # Shade current week column
    ax.axvspan(n - 1.5, n - 0.5, color=C["blue"], alpha=0.08, label="Current Week")

    # Rolling average dashed line
    ax.plot(x, weekly["rolling_avg"], "--", color=C["muted"],
            linewidth=1.8, alpha=0.8, label="4-Week Avg", zorder=2)

    # Main sales line
    ax.plot(x, weekly["sales_k"], color=C["navy"], linewidth=2.5,
            marker="o", markersize=7, markerfacecolor="white",
            markeredgewidth=2.5, markeredgecolor=C["navy"],
            label="Weekly Sales", zorder=3)

    # Highlight current week point in accent color
    ax.plot(n - 1, weekly["sales_k"].iloc[-1], "o",
            color=C["blue"], markersize=11, zorder=4)

    # X-axis labels: week dates
    labels = [d.strftime("%b %d") for d in weekly["week_start_date"]]
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=38, ha="right", fontsize=8.5)

    ax.set_ylabel("Sales ($K)", fontsize=10, labelpad=8)
    ax.set_title("Weekly Sales Trend — 13-Week Overview",
                 fontsize=13, fontweight="bold", color=C["navy"], pad=12)
    ax.legend(fontsize=9, framealpha=0.7, loc="upper left")
    ax.grid(axis="y", linewidth=0.7)
    ax.grid(axis="x", alpha=0)

    plt.tight_layout()
    path = os.path.join(output_dir, "chart_trend.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=C["background"])
    plt.close()
    print(f"   [SUCCESS] Trend chart saved: {path}")
    return path


# ── Chart 2: Category Comparison Bar Chart ────────────────────────────

def create_category_chart(df: pd.DataFrame, output_dir: str) -> str:
    """
    Horizontal bar chart comparing this week's category sales
    against the historical average.

    Visual features:
      - Accent-colored bars for current week
      - Translucent gray bars for historical average (overlaid)
      - Red/orange coloring for anomalous categories (>30% deviation)
      - Dollar values labeled on bars

    Returns: file path to saved PNG
    """
    _ensure_dir(output_dir)

    all_weeks = sorted(df["week_start_date"].unique())
    current_week = all_weeks[-1]
    hist_weeks = all_weeks[-(Config.LOOKBACK_WEEKS + 1):-1]

    current_df = df[df["week_start_date"] == current_week]
    hist_df = df[df["week_start_date"].isin(hist_weeks)]

    # Sales by category
    current_by_cat = (
        current_df.groupby("category")["sales_amount"]
        .sum()
        .sort_values(ascending=True)
    )
    hist_avg_by_cat = (
        hist_df.groupby(["week_start_date", "category"])["sales_amount"]
        .sum()
        .groupby("category")
        .mean()
    )

    categories = current_by_cat.index.tolist()
    current_vals = [current_by_cat[c] / 1000 for c in categories]
    hist_vals = [hist_avg_by_cat.get(c, 0) / 1000 for c in categories]

    # Determine bar colors — flag anomalous categories
    bar_colors = []
    for cur, hist in zip(current_vals, hist_vals):
        if hist > 0:
            dev = (cur - hist) / hist
            if dev >= 0.30:
                bar_colors.append(C["orange"])
            elif dev <= -0.30:
                bar_colors.append(C["red"])
            else:
                bar_colors.append(C["blue"])
        else:
            bar_colors.append(C["blue"])

    y = range(len(categories))
    fig, ax = plt.subplots(figsize=(9, 4.2))

    # Historical average bars (background reference)
    ax.barh(y, hist_vals, height=0.55, color=C["muted"],
            alpha=0.3, label=f"{Config.LOOKBACK_WEEKS}-Week Avg")

    # Current week bars
    bars = ax.barh(y, current_vals, height=0.55, color=bar_colors,
                   alpha=0.88, label="This Week")

    # Value labels on bars
    for i, (bar, val) in enumerate(zip(bars, current_vals)):
        ax.text(val + max(current_vals) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"${val:.1f}K", va="center", ha="left", fontsize=9,
                color=C["text"], fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(categories, fontsize=10)
    ax.set_xlabel("Sales ($K)", fontsize=10)
    ax.set_title("Sales by Category — This Week vs. Historical Average",
                 fontsize=12, fontweight="bold", color=C["navy"], pad=10)

    legend_patches = [
        mpatches.Patch(color=C["blue"], label="This Week (normal)"),
        mpatches.Patch(color=C["orange"], label="This Week (SPIKE)"),
        mpatches.Patch(color=C["red"], label="This Week (DROP)"),
        mpatches.Patch(color=C["muted"], alpha=0.5, label="Historical Avg"),
    ]
    ax.legend(handles=legend_patches, fontsize=8.5, loc="lower right")
    ax.grid(axis="x", linewidth=0.7)
    ax.grid(axis="y", alpha=0)

    plt.tight_layout()
    path = os.path.join(output_dir, "chart_category.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=C["background"])
    plt.close()
    print(f"   [SUCCESS] Category chart saved: {path}")
    return path


# ── Chart 3: Deviation Heatmap ────────────────────────────────────────

def create_heatmap(df: pd.DataFrame, output_dir: str) -> str:
    """
    Heatmap grid showing % deviation from historical average
    for each Category × Region combination.

    Visual features:
      - Red-to-Green colormap centered at 0%
      - Percentage values labeled in each cell
      - Bold text for anomalous cells (>30% deviation)
      - Clean grid lines between cells

    Returns: file path to saved PNG
    """
    _ensure_dir(output_dir)

    all_weeks = sorted(df["week_start_date"].unique())
    current_week = all_weeks[-1]
    hist_weeks = all_weeks[-(Config.LOOKBACK_WEEKS + 1):-1]

    current_df = df[df["week_start_date"] == current_week]
    hist_df = df[df["week_start_date"].isin(hist_weeks)]

    categories = sorted(df["category"].unique())
    regions = sorted(df["region"].unique())

    # Build deviation matrix
    matrix = np.zeros((len(categories), len(regions)))
    for i, cat in enumerate(categories):
        for j, reg in enumerate(regions):
            cur = float(
                current_df[
                    (current_df["category"] == cat) &
                    (current_df["region"] == reg)
                ]["sales_amount"].sum()
            )
            hist = hist_df[
                (hist_df["category"] == cat) &
                (hist_df["region"] == reg)
            ].groupby("week_start_date")["sales_amount"].sum().mean()

            if hist > 0 and not np.isnan(hist):
                matrix[i, j] = ((cur - hist) / hist) * 100
            else:
                matrix[i, j] = 0.0

    # Custom diverging colormap: red → white → green
    cmap = LinearSegmentedColormap.from_list(
        "nar8", [C["red"], "#FFFFFF", C["green"]]
    )

    fig, ax = plt.subplots(figsize=(7, 4.5))

    im = ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=-80, vmax=80)

    # Cell labels
    for i in range(len(categories)):
        for j in range(len(regions)):
            val = matrix[i, j]
            text_color = "white" if abs(val) > 50 else C["text"]
            weight = "bold" if abs(val) >= 30 else "normal"
            ax.text(j, i, f"{val:+.0f}%",
                    ha="center", va="center",
                    fontsize=10, color=text_color, fontweight=weight)

    # Axis labels
    ax.set_xticks(range(len(regions)))
    ax.set_xticklabels(regions, fontsize=10, fontweight="bold")
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories, fontsize=10)

    ax.set_title("Sales Deviation Heatmap — Category × Region",
                 fontsize=12, fontweight="bold", color=C["navy"], pad=12)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label("% vs. Historical Average", fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    # Grid lines between cells
    ax.set_xticks(np.arange(-0.5, len(regions), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(categories), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", size=0)

    plt.tight_layout()
    path = os.path.join(output_dir, "chart_heatmap.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=C["background"])
    plt.close()
    print(f"   [SUCCESS] Heatmap saved: {path}")
    return path


# ── Convenience Function ──────────────────────────────────────────────

def generate_all_charts(df: pd.DataFrame, output_dir: str = None) -> dict:
    """
    Generates all three charts and returns their file paths as a dict.

    Args:
        df: Full sales DataFrame
        output_dir: Where to save PNGs (defaults to Config.CHARTS_DIR)

    Returns:
        {"trend": path, "category": path, "heatmap": path}
    """
    charts_dir = output_dir or Config.CHARTS_DIR
    _ensure_dir(charts_dir)

    print("Generating charts...")
    return {
        "trend":    create_trend_chart(df, charts_dir),
        "category": create_category_chart(df, charts_dir),
        "heatmap":  create_heatmap(df, charts_dir),
    }
