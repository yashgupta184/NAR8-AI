# config/settings.py
"""
NAR8 AI — Configuration Module
Reads all settings from environment variables (.env file).
This is the single source of truth for configuration across the entire project.
"""
import os
from dotenv import load_dotenv

# Load the .env file — must be called before reading any os.getenv()
load_dotenv()


class Config:
    """
    Central configuration class.
    All other modules import this class and read settings from it.
    Never hardcode API keys or paths anywhere else in the project.
    """

    # ── Application Identity ──────────────────────────────────────
    APP_NAME: str = os.getenv("APP_NAME", "NAR8 AI")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    APP_TAGLINE: str = "From raw data to boardroom narrative — automatically."

    # ── LLM Settings ─────────────────────────────────────────────
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    LLM_TEMPERATURE: float = 0.4
    LLM_MAX_TOKENS: int = 2500

    # ── Power BI Settings ────────────────────────────────────────
    USE_MOCK_DATA: bool = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
    POWERBI_CLIENT_ID: str = os.getenv("POWERBI_CLIENT_ID", "")
    POWERBI_CLIENT_SECRET: str = os.getenv("POWERBI_CLIENT_SECRET", "")
    POWERBI_TENANT_ID: str = os.getenv("POWERBI_TENANT_ID", "")
    POWERBI_WORKSPACE_ID: str = os.getenv("POWERBI_WORKSPACE_ID", "")
    POWERBI_DATASET_ID: str = os.getenv("POWERBI_DATASET_ID", "")

    # ── Anomaly Detection Defaults ───────────────────────────────
    Z_SCORE_THRESHOLD: float = 2.0
    PCT_CHANGE_THRESHOLD: float = 0.30
    LOOKBACK_WEEKS: int = 8
    MIN_WEEKS_FOR_DETECTION: int = 4

    # ── Output Settings ──────────────────────────────────────────
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output/slides")
    CHARTS_DIR: str = "output/slides/charts"

    # ── Brand Colors (used in charts and slides) ─────────────────
    COLOR_PRIMARY: str = "#1E3A5F"
    COLOR_ACCENT: str = "#2E86AB"
    COLOR_SUCCESS: str = "#27AE60"
    COLOR_DANGER: str = "#E74C3C"
    COLOR_WARNING: str = "#F39C12"
    COLOR_BACKGROUND: str = "#F8FAFC"
    COLOR_TEXT: str = "#1A1A2E"
    COLOR_MUTED: str = "#95A5A6"

    # ── Data Constants ───────────────────────────────────────────
    WEEKS_OF_DATA: int = 13
    PRODUCT_CATEGORIES: list = ["Electronics", "Apparel", "Home & Garden", "Sports"]
    REGIONS: list = ["North", "South", "West"]

    @classmethod
    def validate(cls) -> list:
        """
        Checks that required settings are present.
        Returns a list of warning messages — empty list means all good.
        """
        warnings = []
        if not cls.USE_MOCK_DATA:
            required_pbi = [
                cls.POWERBI_CLIENT_ID,
                cls.POWERBI_CLIENT_SECRET,
                cls.POWERBI_TENANT_ID,
                cls.POWERBI_WORKSPACE_ID,
                cls.POWERBI_DATASET_ID,
            ]
            if not all(required_pbi):
                warnings.append("Power BI credentials incomplete. Switch to mock data or fill all PBI env vars.")

        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            warnings.append("OPENAI_API_KEY is missing. Add it to your .env file.")
        if cls.LLM_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            warnings.append("ANTHROPIC_API_KEY is missing. Add it to your .env file.")

        return warnings
