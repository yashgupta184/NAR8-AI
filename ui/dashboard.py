# ui/dashboard.py
"""
NAR8 AI — Streamlit Web Dashboard

A highly refined, premium dark-mode interface for the NAR8 AI pipeline.
Features glassmorphism, modern typography (Outfit), and elegant layouts.

Run with:
    streamlit run ui/dashboard.py
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
    page_title="NAR8 AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Premium Font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, .stText {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Hide default Streamlit noise */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* Custom Header */
    .custom-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0rem 0 1.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 2.5rem;
    }
    .header-logo {
        font-weight: 700;
        font-size: 1.3rem;
        color: #F8FAFC;
        letter-spacing: 0.5px;
    }
    .header-logo span { color: #00E5FF; }
    .header-links a {
        color: #94A3B8;
        text-decoration: none;
        margin-left: 2rem;
        font-size: 0.95rem;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    .header-links a:hover { color: #00E5FF; }

    /* Custom Footer */
    .custom-footer {
        margin-top: 6rem;
        padding-top: 2rem;
        padding-bottom: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }
    .footer-brand {
        font-weight: 700;
        font-size: 1.2rem;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }
    .footer-brand span { color: #00E5FF; }
    .footer-text { color: #64748B; font-size: 0.9rem; max-width: 450px; line-height: 1.5; }
    .footer-copyright { color: #475569; font-size: 0.85rem; font-weight: 500; }

    /* Glassmorphic Header */
    .hero-header {
        background: rgba(19, 28, 45, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    .hero-logo {
        background: linear-gradient(135deg, #00E5FF, #0077FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.1;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.1rem;
        font-weight: 400;
        margin: 0.5rem 0 0 0;
        letter-spacing: 0.5px;
    }

    /* Primary Run Button */
    .stButton > button {
        background: linear-gradient(135deg, #00E5FF 0%, #0077FF 100%);
        color: #0A0F1C;
        font-weight: 700;
        font-size: 1.15rem;
        padding: 0.8rem 0;
        border: none;
        border-radius: 12px;
        width: 100%;
        box-shadow: 0 4px 20px rgba(0, 229, 255, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        box-shadow: 0 8px 30px rgba(0, 229, 255, 0.5);
        transform: translateY(-2px);
        color: #000;
    }

    /* Metric Cards Override */
    [data-testid="stMetric"] {
        background: rgba(19, 28, 45, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border: 1px solid rgba(0, 229, 255, 0.3);
    }
    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #F8FAFC;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Info Cards */
    .info-card {
        background: rgba(19, 28, 45, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 4px solid #00E5FF;
    }
    
    /* Executive Summary Block */
    .exec-summary {
        background: linear-gradient(180deg, rgba(19, 28, 45, 0.8) 0%, rgba(10, 15, 28, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    .exec-headline {
        font-size: 1.8rem;
        font-weight: 600;
        color: #FFFFFF;
        line-height: 1.3;
        margin-bottom: 1rem;
    }
    .exec-tldr {
        color: #CBD5E1;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* Table Styling Override */
    .dataframe {
        border: none !important;
    }
    .dataframe th {
        background-color: #131C2D !important;
        color: #94A3B8 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.85rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    .dataframe td {
        background-color: rgba(19, 28, 45, 0.3) !important;
        color: #E2E8F0 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Feature Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1.5rem;
        margin-top: 1rem;
    }
    .feature-card {
        background: rgba(19, 28, 45, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.8rem;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        background: rgba(19, 28, 45, 0.7);
        border: 1px solid rgba(0, 229, 255, 0.2);
    }
    .feature-icon {
        width: 40px;
        height: 40px;
        margin-bottom: 1rem;
        color: #00E5FF;
    }
    .feature-title {
        color: #FFFFFF;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        color: #94A3B8;
        font-size: 0.9rem;
        line-height: 1.5;
    }

</style>
""", unsafe_allow_html=True)


# ── SVG Icons ────────────────────────────────────────────────────────

ICONS = {
    "data": '''<svg class="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path></svg>''',
    "search": '''<svg class="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"></path></svg>''',
    "brain": '''<svg class="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>''',
    "presentation": '''<svg class="feature-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path></svg>''',
    "download": '''<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 8px;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>'''
}


# ── Helper Functions ──────────────────────────────────────────────────

def run_pipeline_with_progress(config_overrides: dict, custom_df: pd.DataFrame = None) -> dict:
    """Runs the pipeline with real-time Streamlit progress updates."""
    from main import run_pipeline

    # Custom styling for the progress bar container
    st.markdown("""
        <div style="margin-top: 2rem; margin-bottom: 1rem;">
            <span style="color: #00E5FF; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; font-size: 0.85rem;">
                System Status
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()

    stages = [
        (25,  "Authenticating with Power BI REST API..."),
        (50,  "Executing Statistical Anomaly Engine..."),
        (75,  "Synthesizing Executive Narrative via LLM..."),
        (100, "Rendering Final Presentation Deck..."),
    ]

    stage_idx = [0]
    last_update = [time.time()]

    def advance_progress():
        if stage_idx[0] < len(stages) and time.time() - last_update[0] > 0.3:
            pct, msg = stages[stage_idx[0]]
            progress_bar.progress(pct - 5)
            status_text.markdown(f"<div style='color: #94A3B8; font-size: 0.95rem; margin-top: 0.5rem;'>{msg}</div>", unsafe_allow_html=True)
            stage_idx[0] += 1
            last_update[0] = time.time()

    advance_progress()
    time.sleep(0.4)
    advance_progress()

    result = run_pipeline(
        z_threshold=config_overrides.get("z_threshold"),
        pct_threshold=config_overrides.get("pct_threshold"),
        lookback_weeks=config_overrides.get("lookback_weeks"),
        verbose=False,
        custom_df=custom_df,
    )

    for pct, msg in stages[stage_idx[0]:]:
        progress_bar.progress(pct)
        status_text.markdown(f"<div style='color: #94A3B8; font-size: 0.95rem; margin-top: 0.5rem;'>{msg}</div>", unsafe_allow_html=True)
        time.sleep(0.2)

    if result["success"]:
        progress_bar.progress(100)
        status_text.markdown(f"<div style='color: #10B981; font-weight: 500; margin-top: 0.5rem;'>Pipeline execution completed in {result['duration_s']}s</div>", unsafe_allow_html=True)
    else:
        progress_bar.progress(100)
        status_text.markdown(f"<div style='color: #EF4444; font-weight: 500; margin-top: 0.5rem;'>Execution Failed: {result['error']}</div>", unsafe_allow_html=True)

    return result


# ── Main Dashboard ────────────────────────────────────────────────────

def main():
    config = Config()

    # ── Global Header ────────────────────────────────────────────────
    st.markdown("""
    <div class="custom-header">
        <div class="header-logo">NAR8 <span>AI</span></div>
        <div class="header-links">
            <a href="https://github.com/yashgupta184/NAR8-AI" target="_blank">GitHub Repository</a>
            <a href="#">Architecture</a>
            <a href="#">Documentation</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero Section ─────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-header">
        <div>
            <h1 class="hero-logo">NAR8 AI</h1>
            <p class="hero-subtitle">Automated Intelligence & Data Storytelling Platform</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("<h3 style='color: #F8FAFC; margin-bottom: 1.5rem;'>System Configuration</h3>", unsafe_allow_html=True)

        st.markdown("<div style='color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 0.5rem;'>Data Source</div>", unsafe_allow_html=True)
        mode_label = "MOCK DATA (DEMO MODE)" if config.USE_MOCK_DATA else "POWER BI REST API"
        color = "#00E5FF" if config.USE_MOCK_DATA else "#10B981"
        st.markdown(f"<div style='background: rgba(19,28,45,0.8); border: 1px solid rgba(255,255,255,0.05); padding: 0.8rem; border-radius: 8px; border-left: 3px solid {color}; color: #F8FAFC; font-weight: 500; margin-bottom: 1rem;'>{mode_label}</div>", unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload Custom CSV (Optional)", type=["csv"], help="Overrides Power BI / Mock Data if provided. Must have columns: week_start_date, category, region, sales_amount.")
        
        if os.path.exists("template.csv"):
            with open("template.csv", "rb") as f:
                st.download_button("Download CSV Template", data=f, file_name="nar8_template.csv", mime="text/csv", use_container_width=True)

        custom_df = None
        if uploaded_file is not None:
            try:
                custom_df = pd.read_csv(uploaded_file)
                
                # Validation
                required_cols = {'week_start_date', 'category', 'region', 'sales_amount'}
                if not required_cols.issubset(custom_df.columns):
                    st.error(f"Missing required columns. Expected: {', '.join(required_cols)}")
                    custom_df = None
                else:
                    custom_df['week_start_date'] = pd.to_datetime(custom_df['week_start_date'])
                    
                    if len(custom_df['week_start_date'].unique()) < config.MIN_WEEKS_FOR_DETECTION:
                        st.error(f"Not enough history. Need at least {config.MIN_WEEKS_FOR_DETECTION} unique weeks of data.")
                        custom_df = None
                    else:
                        st.success("CSV Uploaded Successfully!")
                        
            except Exception as e:
                st.error(f"Invalid CSV: {e}")
                custom_df = None
        st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

        st.markdown("<div style='color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 0.5rem;'>AI Engine</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background: rgba(19,28,45,0.8); border: 1px solid rgba(255,255,255,0.05); padding: 0.8rem; border-radius: 8px; color: #F8FAFC; margin-bottom: 2rem;'><span style='color: #00E5FF; font-weight: 600;'>{config.LLM_PROVIDER.upper()}</span> <br/> <span style='font-size: 0.85rem; color: #94A3B8;'>{config.LLM_MODEL}</span></div>", unsafe_allow_html=True)

        st.markdown("<div style='color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 1rem;'>Detection Thresholds</div>", unsafe_allow_html=True)
        
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

        st.markdown("<div style='margin-top: 3rem; color: #475569; font-size: 0.8rem;'>NAR8 AI v1.0.0<br/>Enterprise Intelligence Platform</div>", unsafe_allow_html=True)


    # ── Main Content Area ─────────────────────────────────────────────

    # Run button (centered)
    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        run_clicked = st.button("Initialize Analysis Sequence", use_container_width=True)

    # ── Pipeline Results ──────────────────────────────────────────────

    if run_clicked:
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        config_overrides = {
            "z_threshold": z_thresh,
            "pct_threshold": pct_thresh,
            "lookback_weeks": lookback,
        }

        with st.spinner(""):
            result = run_pipeline_with_progress(config_overrides, custom_df=custom_df)

        if not result["success"]:
            st.error(f"Pipeline Execution Failed: {result['error']}")
            st.stop()

        report = result["report"]
        narrative = result["narrative"]
        df = result["df"]
        deck_path = result["deck_path"]

        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

        # ── KPI Metrics Row ───────────────────────────────────────────
        st.markdown("<div class='section-header'>Performance Overview</div>", unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(
                "Total Revenue",
                f"${report.overall_week_sales:,.0f}",
                f"{report.wow_change_pct:+.1f}% WoW"
            )
        with m2:
            vs_hist = ((report.overall_week_sales - report.avg_weekly_sales) / report.avg_weekly_sales * 100)
            st.metric(
                "Vs. Historical Avg",
                f"{vs_hist:+.1f}%",
                "Baseline Variance"
            )
        with m3:
            st.metric("Anomalies Detected", report.total_anomalies, "Data points flagged", delta_color="off")
        with m4:
            st.metric("Critical Alerts", report.high_severity_count, "High Severity", delta_color="inverse")

        # ── Executive Summary ─────────────────────────────────────────
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        exec_sum = narrative.get("executive_summary", {})
        if exec_sum:
            sentiment = exec_sum.get("sentiment", "NEUTRAL")
            accent_color = {
                "POSITIVE": "#10B981", # Emerald
                "NEGATIVE": "#EF4444", # Red
                "MIXED":    "#F59E0B", # Amber
                "NEUTRAL":  "#00E5FF", # Cyan
            }.get(sentiment, "#00E5FF")

            st.markdown(f"""
            <div class="exec-summary" style="border-left: 4px solid {accent_color};">
                <div style="color: {accent_color}; font-size: 0.85rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 0.8rem;">
                    AI Executive Briefing — {sentiment}
                </div>
                <div class="exec-headline">{exec_sum.get('headline', '')}</div>
                <div class="exec-tldr">{exec_sum.get('tldr', '')}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Anomaly Table ─────────────────────────────────────────────
        st.markdown("<div class='section-header'>Anomaly Registry</div>", unsafe_allow_html=True)

        if report.anomalies:
            anomaly_rows = []
            for a in report.anomalies:
                anomaly_rows.append({
                    "Severity":    a.severity,
                    "Direction":   a.direction,
                    "Category":    a.category,
                    "Region":      a.region,
                    "Actual":      f"${a.actual_value:,.0f}",
                    "Expected":    f"${a.expected_value:,.0f}",
                    "Deviation":   f"{a.deviation_pct:+.1f}%",
                    "Z-Score":     f"{a.z_score:.2f}",
                })

            anom_df = pd.DataFrame(anomaly_rows)

            def style_severity(val):
                colors = {
                    "HIGH": "background-color: rgba(239, 68, 68, 0.1); color: #FCA5A5; font-weight: 600;",
                    "MEDIUM": "background-color: rgba(245, 158, 11, 0.1); color: #FCD34D; font-weight: 600;",
                    "LOW": "background-color: rgba(0, 229, 255, 0.1); color: #67E8F9; font-weight: 600;",
                }
                return colors.get(val, "")

            styled = anom_df.style.map(style_severity, subset=["Severity"])
            st.dataframe(styled, use_container_width=True, hide_index=True)
        else:
            st.markdown("""
            <div class="info-card" style="border-left-color: #10B981;">
                <span style="color: #10B981; font-weight: 600;">System Optimal:</span> No significant statistical deviations detected in the current period.
            </div>
            """, unsafe_allow_html=True)

        # ── Two-column layout: Charts preview + Narrative JSON ────────
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        col_a, col_b = st.columns([1.2, 1])

        with col_a:
            st.markdown("<div class='section-header'>Data Visualizations</div>", unsafe_allow_html=True)
            
            import plotly.express as px
            import plotly.graph_objects as go
            
            tabs = st.tabs(["Trend Analysis", "Category Variance", "Regional Heatmap"])
            
            with tabs[0]:
                # Trend Analysis
                weekly = df.groupby("week_start_date")["sales_amount"].sum().reset_index()
                fig1 = px.line(weekly, x="week_start_date", y="sales_amount", markers=True, title="Weekly Sales Trend", template="plotly_dark")
                fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0", margin=dict(l=20, r=20, t=50, b=20))
                fig1.update_traces(line_color="#00E5FF", marker=dict(size=8, color="#00E5FF"))
                st.plotly_chart(fig1, use_container_width=True)

            with tabs[1]:
                # Category Variance
                curr_week = df["week_start_date"].max()
                cat_df = df[df["week_start_date"] == curr_week].groupby("category")["sales_amount"].sum().reset_index()
                fig2 = px.bar(cat_df, x="sales_amount", y="category", orientation='h', title=f"Sales by Category (Week of {curr_week.strftime('%Y-%m-%d')})", template="plotly_dark")
                fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0", margin=dict(l=20, r=20, t=50, b=20))
                fig2.update_traces(marker_color="#00E5FF")
                st.plotly_chart(fig2, use_container_width=True)

            with tabs[2]:
                # Regional Heatmap
                curr_df = df[df["week_start_date"] == curr_week]
                heat_df = curr_df.groupby(["category", "region"])["sales_amount"].sum().unstack()
                fig3 = px.imshow(heat_df, text_auto=".0f", title="Category vs Region Sales", aspect="auto", template="plotly_dark", color_continuous_scale="Blues")
                fig3.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0", margin=dict(l=20, r=20, t=50, b=20))
                st.plotly_chart(fig3, use_container_width=True)

        with col_b:
            st.markdown("<div class='section-header'>Strategic Recommendations</div>", unsafe_allow_html=True)
            
            s5 = narrative.get("slide_5_recommendations", {})
            
            # Action Items
            st.markdown("<div style='color: #00E5FF; font-weight: 600; margin-bottom: 0.5rem;'>Immediate Actions</div>", unsafe_allow_html=True)
            for a in s5.get("immediate", []):
                st.markdown(f"<div style='background: rgba(19,28,45,0.5); padding: 0.8rem 1rem; border-radius: 8px; margin-bottom: 0.5rem; border: 1px solid rgba(255,255,255,0.05); color: #E2E8F0; font-size: 0.95rem;'><span style='color: #00E5FF; margin-right: 8px;'>→</span> {a}</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            # Monitor Items
            st.markdown("<div style='color: #F59E0B; font-weight: 600; margin-bottom: 0.5rem;'>Watchlist for Next Period</div>", unsafe_allow_html=True)
            for m in s5.get("monitor", []):
                st.markdown(f"<div style='background: rgba(19,28,45,0.5); padding: 0.8rem 1rem; border-radius: 8px; margin-bottom: 0.5rem; border: 1px solid rgba(255,255,255,0.05); color: #E2E8F0; font-size: 0.95rem;'><span style='color: #F59E0B; margin-right: 8px;'>•</span> {m}</div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

        # ── Download Section ──────────────────────────────────────────
        
        if deck_path and os.path.exists(deck_path):
            st.markdown("""
            <div style="background: linear-gradient(90deg, rgba(19,28,45,0.8) 0%, rgba(10,15,28,0.8) 100%); border: 1px solid rgba(0,229,255,0.2); border-radius: 16px; padding: 2.5rem; text-align: center;">
                <h3 style="color: #FFFFFF; font-weight: 600; margin-bottom: 0.5rem;">Presentation Deck Generated</h3>
                <p style="color: #94A3B8; margin-bottom: 2rem;">5 Slides • 3 Embedded Visualizations • Enterprise Grade</p>
            </div>
            """, unsafe_allow_html=True)
            
            # We have to use Streamlit's native download button, but we can center it
            col1, col2, col3 = st.columns([1, 1.5, 1])
            with col2:
                # Add a small negative margin to pull it up into the card visually
                st.markdown("<div style='margin-top: -4rem; text-align: center;'>", unsafe_allow_html=True)
                with open(deck_path, "rb") as f:
                    st.download_button(
                        label="DOWNLOAD PPTX DECK",
                        data=f.read(),
                        file_name=os.path.basename(deck_path),
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True,
                    )
                st.markdown("</div>", unsafe_allow_html=True)


    else:
        # ── Landing State — shown before first run ────────────────────
        
        st.markdown("<div class='section-header'>Platform Architecture</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="color: #94A3B8; font-size: 1.05rem; line-height: 1.6; margin-bottom: 2rem; max-width: 900px;">
            NAR8 AI bridges the gap between raw data and strategic business decisions. Built on a modular, decoupled architecture, it ingests quantitative data, identifies statistical anomalies using consensus algorithms, and leverages Generative AI to synthesize boardroom-ready narratives.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="feature-grid">
            <div class="feature-card">
                {ICONS['data']}
                <div class="feature-title">Data Ingestion</div>
                <div class="feature-desc">Connects securely to Microsoft Power BI via OAuth 2.0 to pull comprehensive multi-region sales data.</div>
            </div>
            <div class="feature-card">
                {ICONS['search']}
                <div class="feature-title">Anomaly Engine</div>
                <div class="feature-desc">Executes Z-score, IQR, and rolling average detection algorithms to flag high-fidelity statistical deviations.</div>
            </div>
            <div class="feature-card">
                {ICONS['brain']}
                <div class="feature-title">Generative AI</div>
                <div class="feature-desc">Leverages advanced LLMs (Gemini / OpenAI) to transform mathematical anomalies into strategic narratives.</div>
            </div>
            <div class="feature-card">
                {ICONS['presentation']}
                <div class="feature-title">Automated Reporting</div>
                <div class="feature-desc">Renders precise Matplotlib visualizations and dynamically constructs a boardroom-ready PowerPoint deck.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div class="custom-footer">
       <div class="footer-content">
           <div class="footer-brand">NAR8 <span>AI</span></div>
           <div class="footer-text">Transforming raw data into strategic business narratives autonomously. Developed for modern enterprise intelligence.</div>
       </div>
       <div class="footer-copyright">
           &copy; 2026 NAR8 AI Project. Released under Open Source.
       </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
