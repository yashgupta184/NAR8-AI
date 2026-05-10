# engine/llm_narrator.py
"""
NAR8 AI — LLM Narrative Generator

Takes an AnomalyReport and generates a structured, JSON-format
business narrative using an LLM API. 

Supports free options like Google Gemini (via OpenAI compatibility layer) 
or Groq, as well as OpenAI GPT-4o-mini.

The output JSON maps directly to the 5-slide PowerPoint structure.
"""
import json
import os
from engine.anomaly_detector import AnomalyReport
from config.settings import Config


class LLMNarrator:
    """
    Builds a precision-engineered prompt from an AnomalyReport,
    calls the configured LLM API, and returns a structured dict
    ready for the slide builder.
    """

    def __init__(self):
        self.config = Config()

    def _build_prompt(self, report: AnomalyReport) -> str:
        """
        Constructs the full prompt string.
        All data values are injected directly — no LLM guessing.
        """

        anomaly_text = ""
        for i, a in enumerate(report.anomalies[:6], 1):  # Cap at 6 anomalies
            anomaly_text += f"""
  [{i}] {a.severity} SEVERITY — {a.direction}
      Segment:   {a.category} — {a.region}
      Actual:    ${a.actual_value:,.2f}
      Expected:  ${a.expected_value:,.2f} ({report.baseline_weeks_used}-week avg)
      Deviation: {a.deviation_pct:+.1f}%
      Z-Score:   {a.z_score}
      Methods:   {a.methods_triggered}/3 detection methods triggered
"""

        if not anomaly_text:
            anomaly_text = "  No statistically significant anomalies detected this week."

        prompt = f"""You are a Senior Business Intelligence Analyst at a top-tier consulting firm.
You write weekly sales intelligence reports for C-suite executives.
Your writing is precise, data-driven, and direct. You never use hollow filler phrases
like "it is worth noting", "interestingly", or "it should be mentioned."
Every sentence you write contains a specific number, a business implication, or an action.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NAR8 AI — WEEKLY SALES INTELLIGENCE DATA PACKET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REPORT METADATA:
  Week Analyzed:     {report.week_analyzed}
  Generated:         {report.analysis_datetime}
  Data Source:       {report.data_source}
  Baseline Period:   Last {report.baseline_weeks_used} weeks

OVERALL PERFORMANCE:
  This Week Total:   ${report.overall_week_sales:,.2f}
  Last Week Total:   ${report.previous_week_sales:,.2f}
  Week-over-Week:    {report.wow_change_pct:+.1f}% ({report.wow_direction})
  Avg Weekly Sales:  ${report.avg_weekly_sales:,.2f} (historical)
  Top Segment:       {report.top_segment['name']} — ${report.top_segment['sales']:,.2f} ({report.top_segment['vs_avg_pct']:+.1f}% vs avg)
  Weakest Segment:   {report.bottom_segment['name']} — ${report.bottom_segment['sales']:,.2f} ({report.bottom_segment['vs_avg_pct']:+.1f}% vs avg)
  Segments Checked:  {report.total_segments_checked}

ANOMALIES DETECTED ({report.total_anomalies} total | {report.high_severity_count} HIGH | {report.medium_severity_count} MEDIUM | {report.low_severity_count} LOW):
{anomaly_text}
DETECTION METHODOLOGY:
  Three-method consensus: Z-Score (threshold ±2.0) + IQR fence + Rolling avg deviation (±30%)
  An anomaly is flagged only when >=2 of 3 methods agree — reducing false positives.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR TASK:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generate a complete NAR8 AI Data Story for a 5-slide executive presentation.

CRITICAL FORMATTING RULES:
1. Output ONLY a valid JSON object. No preamble. No markdown. No explanation.
2. Start your response with {{ and end with }}
3. Every bullet point must contain at least one specific number or percentage
4. Keep all narrative text concise — executives read fast
5. Anomaly hypotheses should be realistic business explanations, not generic

Use EXACTLY this JSON structure:

{{
  "executive_summary": {{
    "headline": "One punchy sentence, max 15 words, capturing the single biggest story",
    "tldr": "2-3 sentences. Lead with the most important number. End with what matters most.",
    "sentiment": "POSITIVE | NEGATIVE | MIXED | NEUTRAL",
    "confidence": "HIGH | MEDIUM"
  }},
  "slide_1_title": {{
    "main_title": "NAR8 AI — Weekly Sales Intelligence",
    "subtitle": "Week of {report.week_analyzed} | AI-Powered Analysis by NAR8 AI",
    "kpi_cards": [
      {{
        "label": "Total Revenue",
        "value": "${report.overall_week_sales:,.0f}",
        "delta": "{report.wow_change_pct:+.1f}%",
        "delta_direction": "{report.wow_direction}"
      }},
      {{
        "label": "vs. Historical Avg",
        "value": "{((report.overall_week_sales - report.avg_weekly_sales) / (report.avg_weekly_sales if report.avg_weekly_sales else 1) * 100):+.1f}%",
        "delta": "",
        "delta_direction": "{'UP' if report.overall_week_sales > report.avg_weekly_sales else 'DOWN'}"
      }},
      {{
        "label": "Anomalies Found",
        "value": "{report.total_anomalies}",
        "delta": "{report.high_severity_count} HIGH",
        "delta_direction": "{'DOWN' if report.high_severity_count == 0 else 'UP'}"
      }}
    ]
  }},
  "slide_2_overview": {{
    "title": "Performance at a Glance",
    "narrative": "3-4 sentence paragraph. Include total revenue, WoW change, and the historical comparison. Set context for why the anomalies matter.",
    "bullets": [
      "Specific finding with a number — strongest performance area",
      "Specific finding with a number — concern or notable pattern",
      "Specific finding with a number — context about the week overall"
    ]
  }},
  "slide_3_anomalies": {{
    "title": "Anomalies Detected This Week",
    "intro": "One sentence framing what the anomalies mean collectively for the business.",
    "cards": [
      {{
        "title": "Max 5 words",
        "segment": "Category — Region",
        "severity": "HIGH | MEDIUM | LOW",
        "direction": "SPIKE | DROP",
        "finding": "One sentence with exact actual and expected numbers.",
        "hypothesis": "One sentence: most likely business reason for this anomaly.",
        "action": "One concrete action a manager can take by end of this week."
      }}
    ]
  }},
  "slide_4_insights": {{
    "title": "Strategic Insights",
    "insight_1": {{
      "heading": "Short insight title (4-6 words)",
      "body": "2-3 sentences linking the anomalies to broader business patterns or trends."
    }},
    "insight_2": {{
      "heading": "Short insight title (4-6 words)",
      "body": "2-3 sentences. Can reference regional patterns, category trends, or seasonal context."
    }},
    "watchlist": "One forward-looking sentence about what to monitor closely next week."
  }},
  "slide_5_recommendations": {{
    "title": "Recommended Actions",
    "immediate": [
      "Action 1 — specific, with implied owner and timeframe",
      "Action 2",
      "Action 3"
    ],
    "monitor": [
      "Item to watch next week — 1",
      "Item to watch next week — 2"
    ],
    "closing": "One confident, grounded closing sentence for the presentation."
  }}
}}
"""
        return prompt

    def _call_llm(self, prompt: str) -> str:
        """Calls the configured LLM API (OpenAI, Gemini, Groq via OpenAI client)."""
        provider = self.config.LLM_PROVIDER.lower()
        model_name = self.config.LLM_MODEL
        
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Run: pip install openai")

        # Fallback handling for free APIs via OpenAI compatible endpoints
        base_url = None
        api_key = self.config.OPENAI_API_KEY
        
        if provider == "gemini":
            base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
            api_key = os.getenv("GEMINI_API_KEY", api_key)
            if self.config.LLM_MODEL == "gpt-4o-mini":
                model_name = "gemini-2.5-flash"
        elif provider == "groq":
            base_url = "https://api.groq.com/openai/v1"
            api_key = os.getenv("GROQ_API_KEY", api_key)
            model_name = "llama-3.3-70b-versatile"

        client = OpenAI(api_key=api_key, base_url=base_url)

        print(f"Calling {provider.upper()} API ({model_name})...")
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.LLM_TEMPERATURE,
            # Using JSON response format for supported models
            response_format={"type": "json_object"}
        )

        return response.choices[0].message.content

    def generate_narrative(self, report: AnomalyReport) -> dict:
        """Main method to generate the JSON narrative from an anomaly report."""
        prompt = self._build_prompt(report)
        raw_response = self._call_llm(prompt)

        # Robust JSON parsing
        try:
            # Strip out markdown block if LLM added it despite instructions
            clean_response = raw_response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.startswith("```"):
                clean_response = clean_response[3:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
                
            return json.loads(clean_response)
        except json.JSONDecodeError as e:
            print("[ERROR] Failed to parse LLM response as JSON.")
            print(f"Raw Output:\n{raw_response}")
            raise e
