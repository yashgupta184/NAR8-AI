# output/slide_builder.py
"""
NAR8 AI — Slide Deck Builder

Assembles a complete 5-slide PowerPoint presentation using python-pptx.

Slide structure:
  Slide 1: Title + KPI Cards + Brand Identity
  Slide 2: Performance Overview + Trend Chart
  Slide 3: Anomaly Detail Cards + Heatmap
  Slide 4: Strategic Insights + Category Chart
  Slide 5: Recommended Actions + Closing

All positioning uses Inches() units on a 13.33 × 7.5 inch (16:9) canvas.
"""
import os
from datetime import datetime
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import pandas as pd
from config.settings import Config
from engine.anomaly_detector import AnomalyReport


# ── Color Palette (RGBColor format) ──────────────────────────────────

CLR = {
    "navy":        RGBColor(0x1E, 0x3A, 0x5F),
    "blue":        RGBColor(0x2E, 0x86, 0xAB),
    "green":       RGBColor(0x27, 0xAE, 0x60),
    "red":         RGBColor(0xE7, 0x4C, 0x3C),
    "orange":      RGBColor(0xF3, 0x9C, 0x12),
    "white":       RGBColor(0xFF, 0xFF, 0xFF),
    "background":  RGBColor(0xF8, 0xFA, 0xFC),
    "light_blue":  RGBColor(0xEB, 0xF5, 0xFB),
    "light_green": RGBColor(0xEB, 0xFB, 0xEE),
    "light_red":   RGBColor(0xFD, 0xED, 0xEC),
    "light_orange":RGBColor(0xFE, 0xF9, 0xE7),
    "dark_text":   RGBColor(0x1A, 0x1A, 0x2E),
    "mid_gray":    RGBColor(0x88, 0x88, 0x99),
    "light_gray":  RGBColor(0xE2, 0xE8, 0xF0),
    "slate":       RGBColor(0x4A, 0x55, 0x68),
}

# Severity color mapping
SEVERITY_COLOR = {
    "HIGH":   CLR["red"],
    "MEDIUM": CLR["orange"],
    "LOW":    CLR["blue"],
}

SEVERITY_BG = {
    "HIGH":   CLR["light_red"],
    "MEDIUM": CLR["light_orange"],
    "LOW":    CLR["light_blue"],
}


# ── Helper Functions ──────────────────────────────────────────────────

def _add_rect(slide, left, top, width, height, fill_color, line_color=None):
    """Adds a solid-fill rectangle to a slide."""
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(0.5)
    else:
        shape.line.fill.background()
    return shape


def _add_text(
    slide, text, left, top, width, height,
    size=11, bold=False, color=None, align=PP_ALIGN.LEFT,
    font="Calibri", word_wrap=True, italic=False
):
    """Adds a styled text box to a slide."""
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txBox.text_frame
    tf.word_wrap = word_wrap

    p = tf.paragraphs[0]
    p.alignment = align

    run = p.add_run()
    run.text = str(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = font
    if color:
        run.font.color.rgb = color

    return txBox


def _add_image(slide, img_path, left, top, width, height):
    """Adds an image to a slide if the file exists."""
    if os.path.exists(img_path):
        slide.shapes.add_picture(
            img_path,
            Inches(left), Inches(top),
            Inches(width), Inches(height)
        )
    else:
        # Fallback placeholder if image missing
        _add_rect(slide, left, top, width, height, CLR["light_gray"])
        _add_text(slide, f"[Chart not found: {os.path.basename(img_path)}]",
                  left + 0.1, top + height / 2 - 0.2, width - 0.2, 0.4,
                  size=9, color=CLR["mid_gray"], align=PP_ALIGN.CENTER)


def _add_slide_header(slide, title: str, subtitle: str = ""):
    """Adds the standard NAR8 AI header bar to any slide."""
    _add_rect(slide, 0, 0, 13.33, 0.9, CLR["navy"])
    _add_text(slide, title,
              0.3, 0.08, 10.5, 0.72,
              size=22, bold=True, color=CLR["white"])
    if subtitle:
        _add_text(slide, subtitle,
                  11.0, 0.2, 2.1, 0.5,
                  size=8, color=CLR["mid_gray"], align=PP_ALIGN.RIGHT)


def _add_slide_footer(slide, report: AnomalyReport):
    """Adds the NAR8 AI branded footer to any slide."""
    _add_rect(slide, 0, 7.15, 13.33, 0.35, CLR["navy"])
    footer_text = (
        f"NAR8 AI  |  Week of {report.week_analyzed}  |  "
        f"Generated {report.analysis_datetime}  |  "
        f"Powered by Generative AI + Power BI REST API"
    )
    _add_text(slide, footer_text,
              0.2, 7.17, 13.0, 0.28,
              size=7.5, color=CLR["mid_gray"], align=PP_ALIGN.CENTER)


# ── Slide Builder Class ───────────────────────────────────────────────

class SlideBuilder:
    """
    Builds the complete 5-slide NAR8 AI deck.

    Usage:
        builder = SlideBuilder()
        builder.build_title_slide(narrative, report)
        builder.build_overview_slide(narrative, charts)
        builder.build_anomalies_slide(narrative, report, charts)
        builder.build_insights_slide(narrative, charts)
        builder.build_recommendations_slide(narrative, report)
        path = builder.save("output/slides/NAR8_AI_Report.pptx")
    """

    def __init__(self):
        self.prs = Presentation()
        # Set to 16:9 widescreen
        self.prs.slide_width = Inches(13.33)
        self.prs.slide_height = Inches(7.5)
        self._blank = self.prs.slide_layouts[6]  # Blank layout

    def _new_slide(self):
        return self.prs.slides.add_slide(self._blank)

    # ── Slide 1: Title + KPI Cards ────────────────────────────────────

    def build_title_slide(self, narrative: dict, report: AnomalyReport):
        """
        Slide 1: Brand identity, week info, three KPI cards,
        and the AI-generated executive headline.
        """
        slide = self._new_slide()

        # Full-width navy header (larger than standard)
        _add_rect(slide, 0, 0, 13.33, 2.0, CLR["navy"])

        # NAR8 AI Logo Text
        _add_text(slide, "NAR8 AI",
                  0.4, 0.15, 5, 0.8,
                  size=36, bold=True, color=CLR["white"], font="Calibri")

        # Tagline
        _add_text(slide, "From raw data to boardroom narrative \u2014 automatically.",
                  0.4, 0.92, 8, 0.4,
                  size=11, italic=True,
                  color=RGBColor(0xAD, 0xC8, 0xE6))

        # Report info (right side of header)
        s1 = narrative.get("slide_1_title", {})
        subtitle = s1.get("subtitle", f"Week of {report.week_analyzed}")
        _add_text(slide, subtitle,
                  7.5, 0.2, 5.6, 0.5,
                  size=10, color=RGBColor(0xAD, 0xC8, 0xE6),
                  align=PP_ALIGN.RIGHT)
        _add_text(slide, f"Analysis: {report.analysis_datetime}",
                  7.5, 0.68, 5.6, 0.4,
                  size=9, color=CLR["mid_gray"], align=PP_ALIGN.RIGHT)

        # Executive headline banner
        exec_sum = narrative.get("executive_summary", {})
        headline = exec_sum.get("headline", f"Weekly Sales Report \u2014 {report.week_analyzed}")
        sentiment = exec_sum.get("sentiment", "NEUTRAL")
        banner_color = {
            "POSITIVE": RGBColor(0xEB, 0xFB, 0xEE),
            "NEGATIVE": RGBColor(0xFD, 0xED, 0xEC),
            "MIXED":    RGBColor(0xFE, 0xF9, 0xE7),
            "NEUTRAL":  RGBColor(0xEB, 0xF5, 0xFB),
        }.get(sentiment, CLR["light_blue"])
        headline_text_color = {
            "POSITIVE": CLR["green"],
            "NEGATIVE": CLR["red"],
            "MIXED":    CLR["orange"],
            "NEUTRAL":  CLR["navy"],
        }.get(sentiment, CLR["navy"])

        _add_rect(slide, 0, 2.05, 13.33, 0.85, banner_color)
        sentiment_emoji = {
            "POSITIVE": "P", "NEGATIVE": "N", "MIXED": "M", "NEUTRAL": "-"
        }.get(sentiment, "-")
        _add_text(slide, f"[{sentiment_emoji}]  {headline}",
                  0.4, 2.1, 12.5, 0.75,
                  size=16, bold=True,
                  color=headline_text_color, align=PP_ALIGN.CENTER)

        # KPI Cards
        kpi_cards = s1.get("kpi_cards", [])
        default_cards = [
            {
                "label": "Total Revenue",
                "value": f"${report.overall_week_sales:,.0f}",
                "delta": f"{report.wow_change_pct:+.1f}%",
                "delta_direction": report.wow_direction,
            },
            {
                "label": "vs. Historical Avg",
                "value": f"{((report.overall_week_sales - report.avg_weekly_sales) / report.avg_weekly_sales * 100):+.1f}%",
                "delta": "",
                "delta_direction": "UP" if report.overall_week_sales > report.avg_weekly_sales else "DOWN",
            },
            {
                "label": "Anomalies Found",
                "value": str(report.total_anomalies),
                "delta": f"{report.high_severity_count} HIGH",
                "delta_direction": "DOWN" if report.high_severity_count == 0 else "UP",
            },
        ]
        cards = kpi_cards if kpi_cards else default_cards

        card_colors = [CLR["blue"], CLR["navy"], CLR["red"] if report.high_severity_count > 0 else CLR["green"]]
        card_x_positions = [0.4, 4.75, 9.1]
        card_width = 3.9

        for i, (card, bg_col) in enumerate(zip(cards[:3], card_colors)):
            cx = card_x_positions[i]
            _add_rect(slide, cx, 3.1, card_width, 2.3, bg_col)

            # Card label
            _add_text(slide, card.get("label", ""),
                      cx + 0.18, 3.22, card_width - 0.3, 0.45,
                      size=11, color=RGBColor(0xCC, 0xDD, 0xFF))

            # Main value
            _add_text(slide, card.get("value", ""),
                      cx + 0.18, 3.65, card_width - 0.3, 0.85,
                      size=26, bold=True, color=CLR["white"])

            # Delta / change
            delta = card.get("delta", "")
            if delta:
                direction = card.get("delta_direction", "")
                arrow = "UP" if direction == "UP" else ("DOWN" if direction == "DOWN" else "")
                delta_color = CLR["light_green"] if direction == "UP" else (
                    CLR["light_red"] if direction == "DOWN" else CLR["white"]
                )
                # Use RGB for these since they're on colored backgrounds
                delta_clr = RGBColor(0xCC, 0xFF, 0xCC) if direction == "UP" else (
                    RGBColor(0xFF, 0xCC, 0xCC) if direction == "DOWN" else CLR["white"]
                )
                _add_text(slide, f"{arrow} {delta}",
                          cx + 0.18, 4.5, card_width - 0.3, 0.45,
                          size=13, bold=True, color=delta_clr)

        # TL;DR summary box
        tldr = exec_sum.get("tldr", "")
        if tldr:
            _add_rect(slide, 0, 5.55, 13.33, 1.32, RGBColor(0xF0, 0xF4, 0xFF))
            _add_text(slide, "EXECUTIVE SUMMARY",
                      0.35, 5.6, 3.5, 0.38,
                      size=8.5, bold=True, color=CLR["navy"])
            _add_text(slide, tldr,
                      0.35, 5.97, 12.5, 0.85,
                      size=10.5, color=CLR["dark_text"])

        _add_slide_footer(slide, report)

    # ── Slide 2: Performance Overview ─────────────────────────────────

    def build_overview_slide(self, narrative: dict, report: AnomalyReport, charts: dict):
        """
        Slide 2: AI-written performance narrative, bullet points,
        and the weekly trend line chart.
        """
        slide = self._new_slide()
        s2 = narrative.get("slide_2_overview", {})

        _add_slide_header(slide, s2.get("title", "Performance at a Glance"),
                          f"Week of {report.week_analyzed}")

        # Narrative paragraph
        _add_text(slide, s2.get("narrative", ""),
                  0.3, 1.05, 6.8, 2.2,
                  size=10.5, color=CLR["dark_text"], word_wrap=True)

        # Bullet points
        bullets = s2.get("bullets", [])
        bullet_y = 3.35
        for b in bullets[:4]:
            _add_rect(slide, 0.3, bullet_y, 0.06, 0.38, CLR["blue"])
            _add_text(slide, b,
                      0.5, bullet_y, 6.55, 0.45,
                      size=10, color=CLR["dark_text"])
            bullet_y += 0.55

        # Week stats summary strip
        _add_rect(slide, 0.3, 5.3, 6.7, 1.55, CLR["light_blue"])
        stats = [
            ("This Week", f"${report.overall_week_sales:,.0f}"),
            ("Last Week",  f"${report.previous_week_sales:,.0f}"),
            ("WoW Change", f"{report.wow_change_pct:+.1f}%"),
            ("Hist. Avg",  f"${report.avg_weekly_sales:,.0f}"),
        ]
        for i, (label, val) in enumerate(stats):
            sx = 0.5 + i * 1.65
            _add_text(slide, label,
                      sx, 5.42, 1.55, 0.35,
                      size=8.5, color=CLR["navy"], bold=True)
            val_color = CLR["green"] if "+" in val else (
                CLR["red"] if "-" in val and "%" in val else CLR["dark_text"]
            )
            _add_text(slide, val,
                      sx, 5.75, 1.55, 0.55,
                      size=15, bold=True, color=val_color)

        # Trend chart (right side)
        _add_image(slide, charts.get("trend", ""), 7.2, 0.95, 5.9, 5.1)

        _add_slide_footer(slide, report)

    # ── Slide 3: Anomaly Cards ────────────────────────────────────────

    def build_anomalies_slide(self, narrative: dict, report: AnomalyReport, charts: dict):
        """
        Slide 3: Color-coded anomaly detail cards and deviation heatmap.
        """
        slide = self._new_slide()
        s3 = narrative.get("slide_3_anomalies", {})

        _add_slide_header(slide,
                          s3.get("title", "Anomalies Detected This Week"),
                          f"{report.total_anomalies} anomalies | {report.high_severity_count} HIGH")

        # Intro sentence
        intro = s3.get("intro", "")
        if intro:
            _add_text(slide, intro,
                      0.3, 0.98, 7.6, 0.45,
                      size=10, italic=True, color=CLR["slate"])

        # Anomaly cards
        cards_data = s3.get("cards", [])
        if not cards_data and report.anomalies:
            # Fallback: build cards from report directly
            cards_data = [
                {
                    "title":    f"{a.direction}: {a.category}",
                    "segment":  f"{a.category} \u2014 {a.region}",
                    "severity": a.severity,
                    "direction": a.direction,
                    "finding":  a.description,
                    "hypothesis": "Pending business context verification.",
                    "action":   "Investigate with regional sales manager.",
                }
                for a in report.anomalies[:3]
            ]

        card_y = 1.52
        for card in cards_data[:3]:
            sev = card.get("severity", "MEDIUM")
            bg_clr = SEVERITY_BG.get(sev, CLR["light_blue"])
            stripe_clr = SEVERITY_COLOR.get(sev, CLR["blue"])

            # Card background
            _add_rect(slide, 0.25, card_y, 7.55, 1.72, bg_clr, CLR["light_gray"])
            # Severity stripe on left
            _add_rect(slide, 0.25, card_y, 0.12, 1.72, stripe_clr)

            # Severity badge
            direction_arrow = "UP" if card.get("direction") == "SPIKE" else "DOWN"
            badge_text = f"[{sev}] {direction_arrow} {card.get('direction', '')}"
            _add_text(slide, badge_text,
                      0.48, card_y + 0.07, 3.5, 0.35,
                      size=10, bold=True, color=stripe_clr)

            # Segment
            _add_text(slide, card.get("segment", ""),
                      4.0, card_y + 0.07, 3.7, 0.35,
                      size=10, color=CLR["slate"], align=PP_ALIGN.RIGHT)

            # Finding
            _add_text(slide, card.get("finding", ""),
                      0.48, card_y + 0.44, 7.15, 0.45,
                      size=9.5, color=CLR["dark_text"])

            # Hypothesis label + text
            _add_text(slide, "Hypothesis:",
                      0.48, card_y + 0.90, 1.5, 0.35,
                      size=9, bold=True, color=CLR["navy"])
            _add_text(slide, card.get("hypothesis", ""),
                      1.95, card_y + 0.90, 5.7, 0.35,
                      size=9, italic=True, color=CLR["slate"])

            # Action label + text
            _add_text(slide, "-> Action:",
                      0.48, card_y + 1.27, 1.1, 0.35,
                      size=9, bold=True, color=CLR["navy"])
            _add_text(slide, card.get("action", ""),
                      1.55, card_y + 1.27, 6.1, 0.38,
                      size=9, bold=True, color=CLR["dark_text"])

            card_y += 1.84

        # Heatmap (right side)
        _add_image(slide, charts.get("heatmap", ""), 8.0, 0.95, 5.1, 6.0)

        _add_slide_footer(slide, report)

    # ── Slide 4: Strategic Insights ───────────────────────────────────

    def build_insights_slide(self, narrative: dict, report: AnomalyReport, charts: dict):
        """
        Slide 4: Two strategic insight panels, watchlist item,
        and category comparison chart.
        """
        slide = self._new_slide()
        s4 = narrative.get("slide_4_insights", {})

        _add_slide_header(slide,
                          s4.get("title", "Strategic Insights"),
                          "AI-powered pattern analysis")

        # Insight panels
        insights = [
            s4.get("insight_1", {}),
            s4.get("insight_2", {}),
        ]
        panel_colors = [CLR["light_blue"], RGBColor(0xF0, 0xF5, 0xEB)]
        stripe_colors = [CLR["blue"], CLR["green"]]

        panel_y = 1.02
        for i, (insight, bg, stripe) in enumerate(zip(insights, panel_colors, stripe_colors)):
            if not insight:
                continue
            _add_rect(slide, 0.25, panel_y, 7.35, 1.78, bg, CLR["light_gray"])
            _add_rect(slide, 0.25, panel_y, 0.1, 1.78, stripe)

            _add_text(slide, insight.get("heading", ""),
                      0.48, panel_y + 0.1, 7.0, 0.45,
                      size=12, bold=True, color=CLR["navy"])
            _add_text(slide, insight.get("body", ""),
                      0.48, panel_y + 0.58, 7.0, 1.08,
                      size=10, color=CLR["dark_text"], word_wrap=True)
            panel_y += 1.95

        # Watchlist strip
        watchlist = s4.get("watchlist", "")
        if watchlist:
            _add_rect(slide, 0.25, 5.0, 7.35, 0.72, RGBColor(0xFE, 0xF9, 0xE7),
                      CLR["orange"])
            _add_text(slide, "[WATCH]  WATCH NEXT WEEK",
                      0.45, 5.06, 2.5, 0.32,
                      size=8.5, bold=True, color=CLR["orange"])
            _add_text(slide, watchlist,
                      0.45, 5.37, 7.0, 0.32,
                      size=10, bold=True, color=CLR["dark_text"])

        # Category chart (right side)
        _add_image(slide, charts.get("category", ""), 7.8, 0.95, 5.3, 5.8)

        _add_slide_footer(slide, report)

    # ── Slide 5: Recommendations ──────────────────────────────────────

    def build_recommendations_slide(self, narrative: dict, report: AnomalyReport):
        """
        Slide 5: Two-column layout — immediate actions and monitor list,
        plus a closing statement banner.
        """
        slide = self._new_slide()
        s5 = narrative.get("slide_5_recommendations", {})

        _add_slide_header(slide,
                          s5.get("title", "Recommended Actions"),
                          f"Generated by NAR8 AI \u2014 {report.week_analyzed}")

        # Column 1: Immediate actions
        _add_rect(slide, 0.25, 1.05, 6.15, 0.52, CLR["blue"])
        _add_text(slide, "[ACT]  Act This Week",
                  0.45, 1.1, 5.8, 0.42,
                  size=13, bold=True, color=CLR["white"])

        actions = s5.get("immediate", [])
        action_y = 1.65
        for i, action in enumerate(actions[:4], 1):
            _add_rect(slide, 0.25, action_y, 6.15, 0.78, CLR["light_blue"], CLR["light_gray"])
            _add_text(slide, f"{i}.",
                      0.38, action_y + 0.1, 0.4, 0.58,
                      size=12, bold=True, color=CLR["blue"])
            _add_text(slide, action,
                      0.75, action_y + 0.08, 5.55, 0.65,
                      size=10, color=CLR["dark_text"], word_wrap=True)
            action_y += 0.88

        # Column 2: Monitor list
        _add_rect(slide, 6.85, 1.05, 6.2, 0.52, CLR["orange"])
        _add_text(slide, "[MONITOR]  Monitor Next Week",
                  7.05, 1.1, 5.8, 0.42,
                  size=13, bold=True, color=CLR["white"])

        monitors = s5.get("monitor", [])
        monitor_y = 1.65
        for item in monitors[:3]:
            _add_rect(slide, 6.85, monitor_y, 6.2, 0.82, CLR["light_orange"], CLR["light_gray"])
            _add_text(slide, "-",
                      7.0, monitor_y + 0.12, 0.4, 0.6,
                      size=14, color=CLR["orange"])
            _add_text(slide, item,
                      7.35, monitor_y + 0.1, 5.55, 0.65,
                      size=10, color=CLR["dark_text"], word_wrap=True)
            monitor_y += 0.92

        # Closing statement banner
        closing = s5.get("closing", "NAR8 AI \u2014 Automated intelligence, delivered weekly.")
        _add_rect(slide, 0, 6.58, 13.33, 0.57, CLR["navy"])
        _add_text(slide, f'"{closing}"',
                  0.5, 6.63, 12.3, 0.48,
                  size=12, bold=True, italic=True,
                  color=CLR["white"], align=PP_ALIGN.CENTER)

        _add_slide_footer(slide, report)

    # ── Save ──────────────────────────────────────────────────────────

    def save(self, output_dir: str = None, filename: str = None) -> str:
        """
        Saves the completed presentation to disk.

        Args:
            output_dir: Directory to save in (defaults to Config.OUTPUT_DIR)
            filename: Custom filename (auto-generated if not provided)

        Returns:
            Full path to the saved .pptx file
        """
        save_dir = output_dir or Config.OUTPUT_DIR
        os.makedirs(save_dir, exist_ok=True)

        if not filename:
            date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
            filename = f"NAR8_AI_Report_{date_str}.pptx"

        full_path = os.path.join(save_dir, filename)
        self.prs.save(full_path)
        print(f"[SUCCESS] Slide deck saved: {full_path}")
        return full_path


# ── Master Build Function ─────────────────────────────────────────────

def build_deck(
    narrative: dict,
    report: AnomalyReport,
    df: pd.DataFrame,
    output_dir: str = None
) -> str:
    """
    Orchestrates the complete slide deck build process:
      1. Generates all charts
      2. Builds each slide in order
      3. Saves and returns the file path

    Args:
        narrative: Structured dict from LLMNarrator
        report:    AnomalyReport from AnomalyDetector
        df:        Full sales DataFrame (for chart generation)
        output_dir: Where to save the .pptx

    Returns:
        Path to saved .pptx file
    """
    from output.chart_generator import generate_all_charts

    save_dir = output_dir or Config.OUTPUT_DIR

    # Generate charts first
    charts = generate_all_charts(df, os.path.join(save_dir, "charts"))

    # Build slides
    print("Building slide deck...")
    builder = SlideBuilder()
    builder.build_title_slide(narrative, report)
    builder.build_overview_slide(narrative, report, charts)
    builder.build_anomalies_slide(narrative, report, charts)
    builder.build_insights_slide(narrative, report, charts)
    builder.build_recommendations_slide(narrative, report)

    return builder.save(save_dir)
