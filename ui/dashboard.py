# ui/dashboard.py
"""
NAR8 AI — Streamlit Web Dashboard

The main user-facing interface for NAR8 AI.

Run with:
    streamlit run ui/dashboard.py

Features:
    - Branded landing page
    - Configurable detection thresholds (sidebar)
    - Real-time pipeline progress
    - KPI metrics display
    - Anomaly table with severity color coding
    - AI narrative preview
    - One-click PowerPoint download
"""
import streamlit as st
import pandas as pd
import time
import os
import sys

# Ensure project root is on path (needed when running from ui/ subfolder)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config

# ── Page Config — MUST be the very first Streamlit call ──────────────
st.set_page_config(
    page_title="NAR8 AI — Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide default Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Main header */
    .nar8-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #2E86AB 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(30, 58, 95, 0.25);
    }
    .nar8-header h1 {
        color: white;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .nar8-header p {
        color: #ADC8E6;
        margin: 0.4rem 0 0 0;
        font-size: 1rem;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1rem;
        border-left: 5px solid #2E86AB;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        text-align: center;
    }

    /* Anomaly severity badges */
    .badge-high   { background: #FDECEA; color: #E74C3C; padding: 3px 10px; border-radius: 20px; font-weight: 700; font-size: 0.78rem; }
    .badge-medium { background: #FEF9E7; color: #F39C12; padding: 3px 10px; border-radius: 20px; font-weight: 700; font-size: 0.78rem; }
    .badge-low    { background: #EBF5FB; color: #2E86AB; padding: 3px 10px; border-radius: 20px; font-weight: 700; font-size: 0.78rem; }

    /* Run button */
    .stButton > button {
        background: linear-gradient(135deg, #1E3A5F, #2E86AB);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.75rem 2.5rem;
        border: none;
        border-radius: 10px;
        width: 100%;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(46, 134, 171, 0.4);
        transition: all 0.2s;
    }
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(46, 134, 171, 0.6);
        transform: translateY(-1px);
    }

    /* Step cards */
    .step-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        height: 100%;
    }
    .step-number {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    .step-title {
        font-weight: 700;
        color: #1E3A5F;
        font-size: 1rem;
        margin-bottom: 0.3rem;
    }
    .step-desc {
        color: #718096;
        font-size: 0.88rem;
        line-height: 1.5;
    }

    /* Divider */
    hr { border: none; border-top: 1px solid #E2E8F0; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)


# ── Helper Functions ──────────────────────────────────────────────────

def severity_badge(severity: str) -> str:
    """Returns HTML for a colored severity badge."""
    cls = f"badge-{severity.lower()}"
    return f'<span class="{cls}">{severity}</span>'


def run_pipeline_with_progress(config_overrides: dict) -> dict:
    """
    Runs the pipeline with real-time Streamlit progress updates.

    Args:
        config_overrides: Dict with optional threshold overrides from sidebar

    Returns:
        Pipeline result dict from main.run_pipeline()
    """
    from main import run_pipeline

    progress_bar = st.progress(0, text="🚀 Initializing NAR8 AI pipeline...")
    status_area = st.empty()

    stages = [
        (25,  "📡 Stage 1/4 — Fetching sales data from Power BI..."),
        (50,  "🔍 Stage 2/4 — Running anomaly detection engine..."),
        (75,  "🤖 Stage 3/4 — Generating AI narrative (calling LLM)..."),
        (100, "📊 Stage 4/4 — Building PowerPoint slide deck..."),
    ]

    # We run the actual pipeline in one call, but show fake stage progress
    # to give the user visual feedback during what is a ~20-40 second run
    stage_idx = [0]
    last_update = [time.time()]

    def advance_progress():
        if stage_idx[0] < len(stages) and time.time() - last_update[0] > 0.3:
            pct, msg = stages[stage_idx[0]]
            progress_bar.progress(pct - 5, text=msg)
            status_area.info(msg)
            stage_idx[0] += 1
            last_update[0] = time.time()

    # Advance through first two stages immediately
    advance_progress()
    time.sleep(0.4)
    advance_progress()

    # Run the actual pipeline
    result = run_pipeline(
        z_threshold=config_overrides.get("z_threshold"),
        pct_threshold=config_overrides.get("pct_threshold"),
        lookback_weeks=config_overrides.get("lookback_weeks"),
        verbose=False,
    )

    # Complete remaining stages
    for pct, msg in stages[stage_idx[0]:]:
        progress_bar.progress(pct, text=msg)
        time.sleep(0.2)

    if result["success"]:
        progress_bar.progress(100, text="✅ Pipeline complete!")
        status_area.success(
            f"✅ NAR8 AI analysis complete in {result['duration_s']}s — "
            f"Deck ready for download!"
        )
    else:
        progress_bar.progress(100, text="❌ Pipeline failed")
        status_area.error(f"❌ Error: {result['error']}")

    return result


# ── Main Dashboard ────────────────────────────────────────────────────

def main():
    config = Config()

    # ── Header ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="nar8-header">
        <h1>📊 NAR8 AI</h1>
        <p>Automated Data Storytelling via Generative AI + Power BI REST API</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")

        st.markdown("**Data Source**")
        mode_label = "🟢 Mock Data (Demo Mode)" if config.USE_MOCK_DATA else "🔵 Power BI REST API"
        st.info(mode_label)

        st.markdown("**LLM Provider**")
        st.info(f"{config.LLM_PROVIDER.title()} — `{config.LLM_MODEL}`")

        st.markdown("---")
        st.markdown("**🎛️ Detection Thresholds**")
        st.caption("Adjust how sensitive the anomaly detector is.")

        z_thresh = st.slider(
            "Z-Score Threshold",
            min_value=1.5, max_value=3.5,
            value=float(config.Z_SCORE_THRESHOLD),
            step=0.1,
            help="Higher = less sensitive. Values >|threshold| are flagged."
        )
        pct_thresh = st.slider(
            "% Change Threshold",
            min_value=0.10, max_value=0.60,
            value=float(config.PCT_CHANGE_THRESHOLD),
            step=0.05,
            format="%.0f%%",
            help="Minimum % deviation from rolling average to flag."
        )
        lookback = st.slider(
            "Baseline Lookback (weeks)",
            min_value=4, max_value=12,
            value=int(config.LOOKBACK_WEEKS),
            step=1,
            help="How many historical weeks to use as the normal baseline."
        )

        st.markdown("---")
        st.markdown("**ℹ️ About NAR8 AI**")
        st.caption(
            "NAR8 AI is a generative AI pipeline that automatically detects "
            "weekly sales anomalies and produces executive-ready slide decks. "
            "Built as a data visualization college project."
        )
        st.caption(f"Version {config.APP_VERSION}")

    # ── Main Content Area ─────────────────────────────────────────────

    # Run button (centered)
    col_l, col_mid, col_r = st.columns([1, 2.5, 1])
    with col_mid:
        run_clicked = st.button("🚀  Run Weekly Analysis", use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Pipeline Results ──────────────────────────────────────────────

    if run_clicked:
        config_overrides = {
            "z_threshold": z_thresh,
            "pct_threshold": pct_thresh,
            "lookback_weeks": lookback,
        }

        with st.spinner(""):
            result = run_pipeline_with_progress(config_overrides)

        if not result["success"]:
            st.error(f"Pipeline failed: {result['error']}")
            st.stop()

        report = result["report"]
        narrative = result["narrative"]
        df = result["df"]
        deck_path = result["deck_path"]

        # ── KPI Metrics Row ───────────────────────────────────────────
        st.subheader("📈 This Week at a Glance")
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.metric(
                "Total Revenue",
                f"${report.overall_week_sales:,.0f}",
                f"{report.wow_change_pct:+.1f}% WoW"
            )
        with m2:
            st.metric(
                "vs. Historical Avg",
                f"{((report.overall_week_sales - report.avg_weekly_sales) / report.avg_weekly_sales * 100):+.1f}%",
            )
        with m3:
            st.metric("Anomalies Found", report.total_anomalies)
        with m4:
            st.metric("High Severity", report.high_severity_count,
                      delta_color="inverse")
        with m5:
            st.metric("Week Analyzed", report.week_analyzed)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Executive Summary ─────────────────────────────────────────
        exec_sum = narrative.get("executive_summary", {})
        if exec_sum:
            sentiment = exec_sum.get("sentiment", "NEUTRAL")
            sentiment_emoji = {
                "POSITIVE": "🟢", "NEGATIVE": "🔴",
                "MIXED": "🟡", "NEUTRAL": "⚪"
            }.get(sentiment, "⚪")

            st.markdown(f"### {sentiment_emoji} AI Executive Summary")
            st.markdown(f"**{exec_sum.get('headline', '')}**")
            st.info(exec_sum.get("tldr", ""))

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Anomaly Table ─────────────────────────────────────────────
        st.subheader(f"⚠️ Detected Anomalies ({report.total_anomalies})")

        if report.anomalies:
            anomaly_rows = []
            for a in report.anomalies:
                anomaly_rows.append({
                    "Severity":    a.severity,
                    "Direction":   a.direction,
                    "Category":    a.category,
                    "Region":      a.region,
                    "Actual ($)":  f"${a.actual_value:,.0f}",
                    "Expected ($)": f"${a.expected_value:,.0f}",
                    "Deviation":   f"{a.deviation_pct:+.1f}%",
                    "Z-Score":     f"{a.z_score:.2f}",
                    "Methods":     f"{a.methods_triggered}/3",
                })

            anom_df = pd.DataFrame(anomaly_rows)

            # Color-code the severity column
            def style_severity(val):
                colors = {
                    "HIGH": "background-color: #FDECEA; color: #C0392B; font-weight: bold;",
                    "MEDIUM": "background-color: #FEF9E7; color: #D68910; font-weight: bold;",
                    "LOW": "background-color: #EBF5FB; color: #1A6E91; font-weight: bold;",
                }
                return colors.get(val, "")

            styled = anom_df.style.map(style_severity, subset=["Severity"])
            st.dataframe(styled, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No significant anomalies detected this week. Sales are within normal ranges.")

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Two-column layout: Charts preview + Narrative JSON ────────
        col_a, col_b = st.columns([1.2, 1])

        with col_a:
            st.subheader("📉 Chart Previews")
            charts_dir = os.path.join(Config.OUTPUT_DIR, "charts")
            chart_files = {
                "Weekly Sales Trend": "chart_trend.png",
                "Category Breakdown": "chart_category.png",
                "Deviation Heatmap":  "chart_heatmap.png",
            }
            tabs = st.tabs(list(chart_files.keys()))
            for tab, (label, fname) in zip(tabs, chart_files.items()):
                with tab:
                    fpath = os.path.join(charts_dir, fname)
                    if os.path.exists(fpath):
                        st.image(fpath, use_container_width=True)
                    else:
                        st.caption("Chart not yet generated.")

        with col_b:
            st.subheader("🤖 AI Narrative Preview")
            with st.expander("Executive Summary", expanded=True):
                es = narrative.get("executive_summary", {})
                st.markdown(f"**Headline:** {es.get('headline', '')}")
                st.markdown(f"**Sentiment:** {es.get('sentiment', '')}")
                st.markdown(f"**TL;DR:** {es.get('tldr', '')}")

            with st.expander("Slide 2 — Overview"):
                s2 = narrative.get("slide_2_overview", {})
                st.markdown(s2.get("narrative", ""))
                for b in s2.get("bullets", []):
                    st.markdown(f"- {b}")

            with st.expander("Slide 5 — Recommendations"):
                s5 = narrative.get("slide_5_recommendations", {})
                st.markdown("**Immediate Actions:**")
                for a in s5.get("immediate", []):
                    st.markdown(f"- {a}")
                st.markdown("**Monitor Next Week:**")
                for m in s5.get("monitor", []):
                    st.markdown(f"- {m}")

            with st.expander("Full JSON (Debug View)"):
                import json
                st.code(json.dumps(narrative, indent=2), language="json")

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Download Section ──────────────────────────────────────────
        st.subheader("📥 Download Your Slide Deck")

        if deck_path and os.path.exists(deck_path):
            col_dl, col_info = st.columns([2, 3])
            with col_dl:
                with open(deck_path, "rb") as f:
                    st.download_button(
                        label="⬇️  Download NAR8 AI Report (.pptx)",
                        data=f.read(),
                        file_name=os.path.basename(deck_path),
                        mime=(
                            "application/vnd.openxmlformats-"
                            "officedocument.presentationml.presentation"
                        ),
                        use_container_width=True,
                    )
            with col_info:
                st.markdown(f"""
                **File:** `{os.path.basename(deck_path)}`
                **Slides:** 5 slides
                **Charts:** 3 embedded visualizations
                **Generated:** {report.analysis_datetime}
                **Pipeline time:** {result['duration_s']}s
                """)
        else:
            st.error("Deck file not found. Check the output directory.")

    else:
        # ── Landing State — shown before first run ────────────────────
        st.markdown("### How NAR8 AI Works")

        steps = [
            {
                "emoji": "📡",
                "title": "1. Fetch Data",
                "desc": (
                    "Connects to Microsoft Power BI via REST API using OAuth 2.0 "
                    "authentication and pulls 13 weeks of sales data across all "
                    "categories and regions."
                ),
            },
            {
                "emoji": "🔍",
                "title": "2. Detect Anomalies",
                "desc": (
                    "Three statistical methods — Z-score, IQR fence, and rolling "
                    "average deviation — run simultaneously. Anomalies are flagged "
                    "only when ≥2 methods agree, minimizing false positives."
                ),
            },
            {
                "emoji": "🤖",
                "title": "3. Generate Narrative",
                "desc": (
                    "A precision-engineered prompt sends all anomaly data to an LLM "
                    "(GPT-4o-mini or Claude). The model returns a structured JSON "
                    "business narrative ready for slide assembly."
                ),
            },
            {
                "emoji": "📊",
                "title": "4. Build Slide Deck",
                "desc": (
                    "Matplotlib generates three charts — trend line, category bars, "
                    "and deviation heatmap. python-pptx assembles a branded 5-slide "
                    "PowerPoint deck with all charts, narrative, and recommendations."
                ),
            },
        ]

        cols = st.columns(4)
        for col, step in zip(cols, steps):
            with col:
                st.markdown(f"""
                <div class="step-card">
                    <div class="step-number">{step['emoji']}</div>
                    <div class="step-title">{step['title']}</div>
                    <div class="step-desc">{step['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            "<center><i>Click 'Run Weekly Analysis' above to start the pipeline.</i></center>",
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
