# NAR8 AI — Complete Implementation Plan
## Automated Data Storytelling via Generative AI

> **Project Name:** NAR8 AI
> **Full Title:** Automated Weekly Sales Intelligence — Anomaly Detection & AI-Powered Narrative Slide Deck Generator
> **Difficulty:** Intermediate
> **Total Estimated Time:** 3 weeks part-time / 8–10 days dedicated
> **Resume Value:** ⭐⭐⭐⭐⭐

---

## Table of Contents

1. [Project Identity & Vision](#1-project-identity--vision)
2. [What You Are Building — In Full Detail](#2-what-you-are-building--in-full-detail)
3. [Folder Structure](#3-folder-structure)
4. [Technology Stack](#4-technology-stack)
5. [System Architecture](#5-system-architecture)
6. [External Integrations & One-Time Setup](#6-external-integrations--one-time-setup)
7. [Phase 1 — Project Scaffold & Configuration](#phase-1--project-scaffold--configuration)
8. [Phase 2 — Mock Data Layer & Power BI Connector](#phase-2--mock-data-layer--power-bi-connector)
9. [Phase 3 — Anomaly Detection Engine](#phase-3--anomaly-detection-engine)
10. [Phase 4 — LLM Narrative Generator](#phase-4--llm-narrative-generator)
11. [Phase 5 — Chart Generator](#phase-5--chart-generator)
12. [Phase 6 — Slide Deck Builder](#phase-6--slide-deck-builder)
13. [Phase 7 — Pipeline Orchestrator](#phase-7--pipeline-orchestrator)
14. [Phase 8 — Streamlit Web Dashboard](#phase-8--streamlit-web-dashboard)
15. [Phase 9 — Branding, Polish & GitHub Setup](#phase-9--branding-polish--github-setup)
16. [Testing Checklist](#testing-checklist)
17. [Recommended Timeline](#recommended-timeline)
18. [Resume & LinkedIn Write-Up](#resume--linkedin-write-up)
19. [Troubleshooting Guide](#troubleshooting-guide)

---

## 1. Project Identity & Vision

### Name & Identity

**NAR8 AI** — The "8" replaces "ate" in "Narrate." Short, sharp, tech-forward.
It is a weekly automated business intelligence system that reads sales data, finds what is unusual, and writes the story for you.

### Tagline
*"From raw data to boardroom narrative — automatically."*

### Brand Colors (use these consistently everywhere)
- **Primary Navy:** `#1E3A5F`
- **Accent Blue:** `#2E86AB`
- **Success Green:** `#27AE60`
- **Alert Red:** `#E74C3C`
- **Warning Orange:** `#F39C12`
- **Background Light:** `#F8FAFC`
- **Text Dark:** `#1A1A2E`

---

## 2. What You Are Building — In Full Detail

### The Problem
Every week, business analysts at companies spend 3–6 hours manually:
- Opening Power BI dashboards and reading numbers
- Trying to visually spot what is unusual
- Writing a narrative explaining their findings
- Building a PowerPoint to present to management
- Emailing it out before Monday morning meetings

This is slow, inconsistent, and entirely dependent on one person's time and attention. If that person is busy or misses something, the entire reporting chain breaks down.

### The Solution — NAR8 AI
A fully automated Python pipeline with a web interface that:
1. Connects to Power BI via REST API and pulls 13 weeks of sales data
2. Runs it through a three-method statistical anomaly detection engine
3. Sends the findings to an LLM with a precision-engineered prompt
4. Receives back a complete, structured business narrative in JSON
5. Generates data visualization charts automatically
6. Assembles a fully formatted 5-slide PowerPoint deck
7. Presents everything through a Streamlit web dashboard with a one-click download

### What the User Experience Looks Like
A user opens the NAR8 AI web app in their browser. They see the branded dashboard. They click one button: **"Run Weekly Analysis."** A progress bar appears, showing each step of the pipeline executing in real time. Within 30–45 seconds, the screen fills with: a KPI row showing total revenue and anomaly counts, a table of every detected anomaly with severity labels and deviation percentages, the AI-generated headline and executive summary, and a download button for the PowerPoint deck. They click download, open the file in PowerPoint, and it is a complete, presentation-ready document — slides with charts, narrative text, anomaly cards, strategic insights, and recommended actions. Zero manual work.

---

## 3. Folder Structure

Create exactly this structure on your machine before writing any code:

```
nar8-ai/
│
├── config/
│   ├── __init__.py
│   └── settings.py                  # All configuration, API keys, constants
│
├── data/
│   ├── __init__.py
│   ├── mock_sales_data.py            # Generates realistic fake sales data
│   └── powerbi_connector.py         # Power BI REST API integration
│
├── engine/
│   ├── __init__.py
│   ├── anomaly_detector.py           # Statistical anomaly detection
│   └── llm_narrator.py              # LLM prompt builder & API caller
│
├── output/
│   ├── __init__.py
│   ├── chart_generator.py            # Matplotlib chart creation
│   └── slide_builder.py             # python-pptx slide assembly
│
├── ui/
│   ├── __init__.py
│   └── dashboard.py                 # Streamlit web interface
│
├── assets/
│   └── nar8_logo.png                # Brand logo (you will create this)
│
├── output/
│   └── slides/                      # Auto-created; stores generated decks
│       └── charts/                  # Auto-created; stores chart PNGs
│
├── tests/
│   ├── test_phase1.py
│   ├── test_phase2.py
│   ├── test_phase3.py
│   └── test_phase4.py
│
├── main.py                           # CLI pipeline orchestrator
├── requirements.txt
├── .env                              # Your secrets (never commit this)
├── .env.example                      # Template (safe to commit)
├── .gitignore
└── README.md
```

---

## 4. Technology Stack

| Layer | Tool | Version | Purpose |
|---|---|---|---|
| Language | Python | 3.11+ | Everything |
| Data Manipulation | Pandas | 2.2.2 | DataFrames, grouping, aggregation |
| Math & Stats | NumPy | 1.26.4 | Array operations, Z-scores |
| Statistics | SciPy | 1.13.0 | IQR, statistical functions |
| Data Source | Power BI REST API | v1.0 | Real enterprise data extraction |
| Mock Data | Custom generator | — | Simulates Power BI for offline dev |
| LLM (Option A) | OpenAI GPT-4o-mini | Latest | Narrative generation (cheap) |
| LLM (Option B) | Anthropic Claude | Latest | Narrative generation (alternative) |
| Slide Deck | python-pptx | 0.6.23 | Generate .pptx files |
| Charts | Matplotlib | 3.9.0 | Data visualizations embedded in slides |
| Image Processing | Pillow | 10.3.0 | Image handling for slides |
| Web UI | Streamlit | 1.35.0 | Interactive web dashboard |
| Auth | MSAL | 1.28.0 | Azure AD / Power BI authentication |
| Env Management | python-dotenv | 1.0.1 | Load .env secrets safely |
| HTTP Client | requests | 2.32.0 | API calls |

> **Cost Note:** GPT-4o-mini costs roughly $0.15 per 1M input tokens. One full pipeline run costs under $0.01. Your entire development and testing will cost under $2 total.

---

## 5. System Architecture

```
╔══════════════════════════════════════════════════════════════════╗
║                        NAR8 AI SYSTEM                           ║
╚══════════════════════════════════════════════════════════════════╝

  ┌─────────────────────────────────────────────────────────────┐
  │               STREAMLIT WEB DASHBOARD (ui/)                 │
  │   User clicks "Run Analysis" → triggers pipeline            │
  └───────────────────────────┬─────────────────────────────────┘
                              │ calls
                              ▼
  ┌─────────────────────────────────────────────────────────────┐
  │               ORCHESTRATOR (main.py)                        │
  │   Coordinates all 4 pipeline stages in sequence             │
  └──────┬───────────────┬──────────────────┬───────────────────┘
         │               │                  │
         ▼               ▼                  ▼
  ┌────────────┐  ┌─────────────┐  ┌──────────────────────────┐
  │ DATA LAYER │  │  ANOMALY    │  │    LLM NARRATIVE         │
  │            │  │  ENGINE     │  │    ENGINE                │
  │ Power BI   │  │             │  │                          │
  │ REST API   │  │ Z-Score     │  │  Prompt Builder          │
  │    OR      │  │ IQR Method  │  │  ──────────────►         │
  │ Mock Data  │  │ Rolling Avg │  │  OpenAI / Claude API     │
  │            │  │             │  │  ◄──────────────         │
  │ → pandas   │  │ → Anomaly   │  │  JSON Narrative          │
  │ DataFrame  │  │   Report    │  │                          │
  └────────────┘  └─────────────┘  └──────────────────────────┘
         │               │                  │
         └───────────────┴──────────────────┘
                              │ all feed into
                              ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                  OUTPUT GENERATOR                           │
  │                                                             │
  │   chart_generator.py  →  3x Matplotlib PNG charts          │
  │   slide_builder.py    →  5-slide .pptx deck                │
  │                                                             │
  │   NAR8_AI_Report_YYYY-MM-DD.pptx  ← final deliverable      │
  └─────────────────────────────────────────────────────────────┘
```

### Data Flow (step by step)
1. `PowerBIConnector.fetch_weekly_sales()` → returns a pandas DataFrame with 13 weeks × 4 categories × 3 regions = 156 rows
2. `AnomalyDetector.detect(df)` → returns an `AnomalyReport` dataclass with every flagged anomaly
3. `LLMNarrator.generate_narrative(report)` → returns a structured Python dict parsed from the LLM's JSON response
4. `ChartGenerator` functions → return file paths to 3 saved PNG images
5. `SlideBuilder.build_*_slide()` methods → add slides to a `Presentation` object
6. `builder.save(path)` → writes the .pptx to disk
7. Streamlit provides a download button pointing to that file

---

## 6. External Integrations & One-Time Setup

> Read this section completely before touching any code. Do it in order. Each step must be done once and then you are set for the entire project.

### 6.1 Install Python

Go to https://python.org/downloads and download Python 3.11 or 3.12.

During installation on Windows, you **must** check the box that says **"Add Python to PATH"** — if you miss this, Python will not be found in your terminal.

After installation, open a terminal (Command Prompt on Windows, Terminal on Mac) and run:

```bash
python --version
```

You should see something like `Python 3.11.9`. If you see an error, Python is not on your PATH — reinstall and check the box.

---

### 6.2 Install VS Code

Download from https://code.visualstudio.com. After installing:
- Open VS Code
- Press `Ctrl+Shift+X` (Windows) or `Cmd+Shift+X` (Mac) to open Extensions
- Search for "Python" and install the Microsoft Python extension
- Search for "Pylance" and install it — gives you intelligent code completion

---

### 6.3 Create the Project & Virtual Environment

Open your terminal and run these commands one by one:

```bash
# Create the project folder
mkdir nar8-ai
cd nar8-ai

# Create a virtual environment
python -m venv venv

# Activate it — Windows:
venv\Scripts\activate

# Activate it — Mac/Linux:
source venv/bin/activate
```

You will see `(venv)` appear at the start of your terminal prompt. This means you are now working inside the isolated virtual environment. Every package you install goes here, not into your system Python. Always activate the venv before working on this project.

---

### 6.4 Create requirements.txt and Install Packages

Create a file called `requirements.txt` in the `nar8-ai` folder with this exact content:

```
pandas==2.2.2
numpy==1.26.4
scipy==1.13.0
matplotlib==3.9.0
python-pptx==0.6.23
openai==1.30.0
anthropic==0.28.0
streamlit==1.35.0
python-dotenv==1.0.1
requests==2.32.0
msal==1.28.0
Pillow==10.3.0
openpyxl==3.1.2
```

Now install everything:

```bash
pip install -r requirements.txt
```

This will take 2–3 minutes. You will see packages downloading. When it finishes, all tools are ready.

---

### 6.5 Get an LLM API Key

**Option A — OpenAI (recommended for beginners, cheaper)**

1. Go to https://platform.openai.com/signup
2. Create an account (use your personal email, not college email)
3. Go to https://platform.openai.com/billing and add a payment method
4. Add $5 of credit — this is more than enough for the entire project
5. Go to https://platform.openai.com/api-keys
6. Click **"Create new secret key"**
7. Name it: `nar8-ai-key`
8. Copy the key — it starts with `sk-` and you will never see it again after closing that dialog
9. Store it temporarily in a notepad file

**Option B — Anthropic Claude**

1. Go to https://console.anthropic.com
2. Create an account
3. Go to Settings → Billing and add credit
4. Go to API Keys and create a new key
5. Copy the key — it starts with `sk-ant-`

You only need one of these. OpenAI GPT-4o-mini is cheaper and simpler for a first project.

---

### 6.6 Set Up Power BI REST API (Optional but Impressive)

> **Important:** If you do not have a Microsoft 365 work or school account with Power BI Pro, skip this section entirely. Set `USE_MOCK_DATA=true` in your `.env` file and the project works perfectly. Only follow these steps if you have access to a real Power BI workspace.

**Step 1 — Register an App in Azure**

1. Go to https://portal.azure.com and sign in with your Microsoft account
2. In the top search bar, type "App registrations" and click it
3. Click **"+ New registration"**
4. Fill in:
   - Name: `nar8-ai`
   - Supported account types: "Accounts in this organizational directory only"
   - Redirect URI: leave blank
5. Click **Register**
6. You are now on the app's overview page. Copy and save:
   - **Application (client) ID** — looks like `a1b2c3d4-...`
   - **Directory (tenant) ID** — looks like `x1y2z3...`

**Step 2 — Add API Permissions**

1. In the left sidebar, click **"API permissions"**
2. Click **"Add a permission"**
3. Click **"Power BI Service"**
4. Select **"Delegated permissions"**
5. Check these boxes: `Dataset.Read.All`, `Report.Read.All`, `Workspace.Read.All`
6. Click **"Add permissions"**
7. Click **"Grant admin consent for [your organization]"** — requires admin rights on the tenant

**Step 3 — Create a Client Secret**

1. In the left sidebar, click **"Certificates & secrets"**
2. Click **"New client secret"**
3. Description: `nar8-ai-secret`
4. Expiry: 6 months
5. Click **Add**
6. **Immediately copy the Value shown** — it disappears when you navigate away

**Step 4 — Find Your Power BI IDs**

1. Go to https://app.powerbi.com
2. Open the workspace you want to use
3. Look at the URL — it will be: `https://app.powerbi.com/groups/{WORKSPACE_ID}/...`
4. Copy that WORKSPACE_ID
5. Click on your dataset and copy its ID from the URL similarly

---

### 6.7 Create the .env File

In the root `nar8-ai/` folder, create a file called `.env`:

```
# ─── LLM Configuration ───────────────────────────────────────────
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini

# ─── Power BI Configuration ──────────────────────────────────────
USE_MOCK_DATA=true
POWERBI_CLIENT_ID=your-azure-app-client-id
POWERBI_CLIENT_SECRET=your-azure-client-secret
POWERBI_TENANT_ID=your-azure-tenant-id
POWERBI_WORKSPACE_ID=your-workspace-id
POWERBI_DATASET_ID=your-dataset-id

# ─── App Configuration ───────────────────────────────────────────
APP_NAME=NAR8 AI
APP_VERSION=1.0.0
OUTPUT_DIR=output/slides
```

Also create `.env.example` (safe to share/commit — contains no real keys):

```
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
USE_MOCK_DATA=true
POWERBI_CLIENT_ID=
POWERBI_CLIENT_SECRET=
POWERBI_TENANT_ID=
POWERBI_WORKSPACE_ID=
POWERBI_DATASET_ID=
```

---

### 6.8 Create .gitignore

Create `.gitignore` in the root folder:

```
# Environment & Secrets
.env
venv/
__pycache__/
*.pyc
*.pyo

# Output files
output/slides/*.pptx
output/slides/charts/*.png

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
```

---

## Phase 1 — Project Scaffold & Configuration

> **Goal:** Create the project skeleton, all empty files, and the settings module.
> **What you learn:** How professional Python projects are structured; how environment variables work.
> **Estimated time:** 1–2 hours

### What to do

Create all the folders and `__init__.py` files. Every folder that contains Python modules needs an `__init__.py` file — it tells Python to treat that folder as a package, allowing you to import from it.

```bash
# Run these from inside your nar8-ai/ folder
mkdir config data engine output ui assets tests
touch config/__init__.py
touch data/__init__.py
touch engine/__init__.py
touch output/__init__.py
touch ui/__init__.py
touch tests/__init__.py
mkdir output/slides
mkdir output/slides/charts
```

On Windows, replace `touch` with `type nul >` or just create the files manually in VS Code.

### Create `config/settings.py`

This is the single source of truth for all configuration in the project. Every other module imports from here. Notice how we never hardcode values — we always read from environment variables.

```python
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
```

### Phase 1 Test

Create `tests/test_phase1.py`:

```python
# tests/test_phase1.py
from config.settings import Config

def test_config():
    print(f"App Name: {Config.APP_NAME}")
    print(f"LLM Provider: {Config.LLM_PROVIDER}")
    print(f"LLM Model: {Config.LLM_MODEL}")
    print(f"Mock Data Mode: {Config.USE_MOCK_DATA}")
    print(f"Output Dir: {Config.OUTPUT_DIR}")

    warnings = Config.validate()
    if warnings:
        print("\n⚠ Warnings:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("\n✅ All configuration checks passed.")

if __name__ == "__main__":
    test_config()
```

Run: `python tests/test_phase1.py`

Expected output: You see your config values printed and either warnings or a green check.

---

## Phase 2 — Mock Data Layer & Power BI Connector

> **Goal:** Build the data foundation — a realistic mock dataset and the real API connector.
> **What you learn:** Pandas DataFrames, structured data generation, REST API patterns.
> **Estimated time:** 2–3 hours

### Understanding the Data Model

Your data represents 13 weeks of sales across 4 product categories and 3 geographic regions. That gives you 156 rows (13 × 4 × 3). Each row has:

| Column | Type | Description |
|---|---|---|
| week_start_date | datetime | Monday of that week |
| week_number | int | 1 through 13 |
| category | str | Electronics, Apparel, Home & Garden, Sports |
| region | str | North, South, West |
| sales_amount | float | Total dollar sales that week |
| units_sold | int | Number of units |
| avg_order_value | float | sales_amount / units_sold |
| returns_amount | float | Dollar value of returns |

The most recent week (week 13) is "this week" — the one being analyzed.

### Create `data/mock_sales_data.py`

```python
# data/mock_sales_data.py
"""
NAR8 AI — Mock Sales Data Generator

Generates realistic weekly sales data that exactly mimics what the
Power BI REST API would return from a real semantic model.

Why mock data?
  - Lets the project work without a real Power BI account
  - Gives full control over the data (we can plant specific anomalies)
  - Swapping to real API data requires only changing USE_MOCK_DATA=false
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config.settings import Config


def generate_mock_sales_data(
    weeks: int = None,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generates a realistic weekly sales DataFrame.

    Planted anomalies (intentional — so detection always has something to find):
      - Week 8: Electronics – North → 145% sales SPIKE (flash sale event)
      - Week 10: Apparel – South → 72% sales DROP (supply chain issue)
      - Week 12: Sports – West → 65% sales SPIKE (influencer campaign)

    Args:
        weeks: Number of weeks to generate. Defaults to Config.WEEKS_OF_DATA (13)
        seed: Random seed for reproducibility

    Returns:
        pandas DataFrame with columns:
        week_start_date, week_number, category, region,
        sales_amount, units_sold, avg_order_value, returns_amount
    """
    if weeks is None:
        weeks = Config.WEEKS_OF_DATA

    np.random.seed(seed)

    # Base weekly sales per category (realistic retail numbers in USD)
    BASE_SALES = {
        "Electronics":   85000,
        "Apparel":       42000,
        "Home & Garden": 31000,
        "Sports":        28000,
    }

    # Regional multipliers (North is strongest market)
    REGION_FACTOR = {"North": 1.20, "South": 0.90, "West": 1.10}

    # Start date: 13 weeks ago from a fixed reference date
    base_date = datetime(2025, 1, 6)  # A Monday

    records = []

    for week_num in range(weeks):
        week_date = base_date + timedelta(weeks=week_num)

        for category in Config.PRODUCT_CATEGORIES:
            for region in Config.REGIONS:

                # Natural random variation week to week (±15%)
                variation = np.random.normal(1.0, 0.12)

                # Slight upward trend over time (0.8% growth per week)
                trend = 1.0 + (week_num * 0.008)

                # Seasonal effect — slight dip in middle weeks
                seasonal = 1.0 - 0.04 * abs(week_num - (weeks / 2)) / (weeks / 2)

                # ── PLANT ANOMALY 1 ──────────────────────────────
                # Week 8 (index 7): Electronics North — massive spike
                if week_num == 7 and category == "Electronics" and region == "North":
                    variation = 2.45   # +145% above normal

                # ── PLANT ANOMALY 2 ──────────────────────────────
                # Week 10 (index 9): Apparel South — sharp drop
                if week_num == 9 and category == "Apparel" and region == "South":
                    variation = 0.28   # -72% below normal

                # ── PLANT ANOMALY 3 ──────────────────────────────
                # Week 12 (index 11): Sports West — significant spike
                if week_num == 11 and category == "Sports" and region == "West":
                    variation = 1.65   # +65% above normal

                # Calculate final sales
                sales = round(
                    BASE_SALES[category]
                    * variation
                    * trend
                    * seasonal
                    * REGION_FACTOR[region],
                    2
                )
                sales = max(sales, 500)  # Floor at $500

                # Derived metrics
                avg_price = np.random.uniform(45, 150)
                units = max(1, int(sales / avg_price))
                avg_order = round(sales / units, 2)
                returns = round(sales * np.random.uniform(0.01, 0.06), 2)

                records.append({
                    "week_start_date": week_date,
                    "week_number":     week_num + 1,
                    "category":        category,
                    "region":          region,
                    "sales_amount":    sales,
                    "units_sold":      units,
                    "avg_order_value": avg_order,
                    "returns_amount":  returns,
                })

    df = pd.DataFrame(records)
    df["week_start_date"] = pd.to_datetime(df["week_start_date"])
    df = df.sort_values(["week_start_date", "category", "region"]).reset_index(drop=True)

    return df


def get_current_week(df: pd.DataFrame) -> pd.DataFrame:
    """Returns only the most recent week's data."""
    return df[df["week_start_date"] == df["week_start_date"].max()].copy()


def get_previous_week(df: pd.DataFrame) -> pd.DataFrame:
    """Returns the second most recent week's data."""
    weeks = sorted(df["week_start_date"].unique())
    if len(weeks) < 2:
        return pd.DataFrame()
    return df[df["week_start_date"] == weeks[-2]].copy()


def get_historical_baseline(df: pd.DataFrame, lookback: int = 8) -> pd.DataFrame:
    """Returns historical data (excluding current week) for baseline comparison."""
    all_weeks = sorted(df["week_start_date"].unique())
    if len(all_weeks) <= 1:
        return pd.DataFrame()
    historical_weeks = all_weeks[-(lookback + 1):-1]  # Exclude current week
    return df[df["week_start_date"].isin(historical_weeks)].copy()
```

### Create `data/powerbi_connector.py`

```python
# data/powerbi_connector.py
"""
NAR8 AI — Power BI REST API Connector

Handles two modes:
  1. MOCK MODE (USE_MOCK_DATA=true): Returns generated fake data
  2. LIVE MODE (USE_MOCK_DATA=false): Authenticates with Azure AD
     and executes a DAX query against a real Power BI semantic model

Authentication uses OAuth 2.0 Client Credentials Flow:
  - Your Azure App (client_id + client_secret) acts as the identity
  - You exchange these credentials for a Bearer token
  - That token is attached to every Power BI API request
"""
import requests
import pandas as pd
from config.settings import Config
from data.mock_sales_data import generate_mock_sales_data


class PowerBIConnector:
    """
    Abstracts the data source behind a clean interface.
    All other modules call fetch_weekly_sales() and do not
    care whether it came from the API or mock generator.
    """

    def __init__(self):
        self.config = Config()
        self._access_token: str = ""

    def _get_access_token(self) -> str:
        """
        Authenticates with Azure Active Directory using the
        Client Credentials OAuth 2.0 flow and returns a Bearer token.

        This is a machine-to-machine authentication pattern —
        no human login required. Your app proves its identity
        using client_id + client_secret.
        """
        try:
            import msal
        except ImportError:
            raise ImportError("Run: pip install msal")

        authority = f"https://login.microsoftonline.com/{self.config.POWERBI_TENANT_ID}"

        app = msal.ConfidentialClientApplication(
            client_id=self.config.POWERBI_CLIENT_ID,
            client_credential=self.config.POWERBI_CLIENT_SECRET,
            authority=authority,
        )

        result = app.acquire_token_for_client(
            scopes=["https://analysis.windows.net/powerbi/api/.default"]
        )

        if "access_token" not in result:
            error = result.get("error_description", "Unknown error")
            raise ValueError(f"Power BI authentication failed: {error}")

        print("✅ Power BI authentication successful")
        return result["access_token"]

    def _execute_dax_query(self, dax_query: str) -> pd.DataFrame:
        """
        Sends a DAX query to the Power BI Execute Queries API endpoint.

        DAX (Data Analysis Expressions) is Power BI's formula language.
        The Execute Queries API accepts a DAX query string and returns
        results as JSON, which we convert to a pandas DataFrame.

        API Endpoint:
          POST /v1.0/myorg/groups/{workspaceId}/datasets/{datasetId}/executeQueries

        Args:
            dax_query: Valid DAX query string

        Returns:
            pandas DataFrame with query results
        """
        if not self._access_token:
            self._access_token = self._get_access_token()

        url = (
            f"https://api.powerbi.com/v1.0/myorg/groups/"
            f"{self.config.POWERBI_WORKSPACE_ID}/datasets/"
            f"{self.config.POWERBI_DATASET_ID}/executeQueries"
        )

        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "queries": [{"query": dax_query}],
            "serializerSettings": {"includeNulls": True},
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 401:
            # Token may have expired — refresh and retry once
            self._access_token = self._get_access_token()
            headers["Authorization"] = f"Bearer {self._access_token}"
            response = requests.post(url, headers=headers, json=payload, timeout=30)

        response.raise_for_status()

        data = response.json()
        rows = data["results"][0]["tables"][0]["rows"]
        return pd.DataFrame(rows)

    def _parse_powerbi_response(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalizes the raw Power BI API response into the same
        column structure as the mock data generator.

        Power BI returns column names like '[Table].[ColumnName]' —
        we clean and rename them to match our internal schema.
        """
        # Power BI prefixes column names with the table/measure name
        # Adapt these renames to match your actual semantic model column names
        column_map = {
            "[Date].[WeekStartDate]":            "week_start_date",
            "[Product].[Category]":              "category",
            "[Sales Territory].[Region]":        "region",
            "[Measures].[Sales Amount]":          "sales_amount",
            "[Measures].[Units Sold]":            "units_sold",
            "[Measures].[Returns Amount]":        "returns_amount",
        }
        df = df.rename(columns=column_map)
        df["week_start_date"] = pd.to_datetime(df["week_start_date"])
        df["sales_amount"] = pd.to_numeric(df["sales_amount"], errors="coerce").fillna(0)
        df["units_sold"] = pd.to_numeric(df["units_sold"], errors="coerce").fillna(0).astype(int)
        df["returns_amount"] = pd.to_numeric(df["returns_amount"], errors="coerce").fillna(0)

        # Derive avg_order_value if not already present
        if "avg_order_value" not in df.columns:
            df["avg_order_value"] = (
                df["sales_amount"] / df["units_sold"].replace(0, 1)
            ).round(2)

        # Add week number
        min_date = df["week_start_date"].min()
        df["week_number"] = ((df["week_start_date"] - min_date).dt.days // 7 + 1)

        return df

    def fetch_weekly_sales(self, weeks: int = None) -> pd.DataFrame:
        """
        Main public method — fetches weekly sales data.

        In MOCK MODE: returns generated data instantly (no internet needed)
        In LIVE MODE: authenticates with Azure and queries Power BI

        Args:
            weeks: Number of weeks to fetch (default from Config)

        Returns:
            pandas DataFrame with standardized columns
        """
        if weeks is None:
            weeks = Config.WEEKS_OF_DATA

        if self.config.USE_MOCK_DATA:
            print(f"ℹ️  NAR8 AI running in MOCK DATA mode")
            print(f"   (Set USE_MOCK_DATA=false in .env for real Power BI)")
            return generate_mock_sales_data(weeks=weeks)

        print("🔗 Connecting to Power BI REST API...")

        # This DAX query retrieves weekly aggregated sales from the semantic model
        # Adapt the table/column names to match your actual Power BI model
        dax_query = f"""
        EVALUATE
        SUMMARIZECOLUMNS (
            'Date'[WeekStartDate],
            'Product'[Category],
            'Sales Territory'[Region],
            "Sales Amount",   [Total Sales],
            "Units Sold",     [Total Units],
            "Returns Amount", [Total Returns]
        )
        ORDER BY 'Date'[WeekStartDate] ASC
        """

        raw_df = self._execute_dax_query(dax_query)
        df = self._parse_powerbi_response(raw_df)

        print(f"✅ Fetched {len(df)} rows from Power BI")
        return df
```

### Phase 2 Test

Create `tests/test_phase2.py`:

```python
# tests/test_phase2.py
from data.powerbi_connector import PowerBIConnector
from data.mock_sales_data import get_current_week, get_historical_baseline

def test_data_layer():
    connector = PowerBIConnector()
    df = connector.fetch_weekly_sales()

    print(f"\n✅ Data loaded: {len(df)} rows")
    print(f"   Weeks: {df['week_start_date'].nunique()}")
    print(f"   Categories: {df['category'].unique().tolist()}")
    print(f"   Regions: {df['region'].unique().tolist()}")
    print(f"\nSample rows:")
    print(df.head(6).to_string())

    current = get_current_week(df)
    print(f"\nCurrent week total sales: ${current['sales_amount'].sum():,.2f}")

    baseline = get_historical_baseline(df)
    print(f"Baseline rows: {len(baseline)}")

    # Sanity checks
    assert len(df) == 156, f"Expected 156 rows, got {len(df)}"
    assert df['sales_amount'].min() > 0, "Sales amount should never be 0 or negative"
    assert df['week_start_date'].nunique() == 13, "Should have 13 unique weeks"
    print("\n✅ All assertions passed.")

if __name__ == "__main__":
    test_data_layer()
```

Run: `python tests/test_phase2.py`

---

## Phase 3 — Anomaly Detection Engine

> **Goal:** Automatically identify statistically unusual sales patterns.
> **What you learn:** Z-score, IQR, rolling averages, dataclasses, statistical reasoning.
> **Estimated time:** 3–4 hours

### The Three Detection Methods Explained

**Z-Score Analysis**
The Z-score measures how many standard deviations a value is from the historical mean. Formula: `z = (current_value - mean) / std_deviation`. A Z-score of 2.0 means the value is 2 standard deviations from average — about 95% of normal data falls within ±2 standard deviations, so anything beyond ±2 is unusual. We use a threshold of ±2.0 for this project.

**IQR (Interquartile Range) Analysis**
The IQR is the range between the 25th and 75th percentile of historical data. It is more robust than Z-score because it ignores extreme outliers when calculating the expected range. Anything below Q1 − 1.5×IQR or above Q3 + 1.5×IQR is flagged.

**Rolling Average Deviation**
We calculate the average of the last 8 weeks and check how far the current week deviates from it as a percentage. If sales are 30%+ above or below the rolling average, it is flagged. This is the most intuitive method for business users.

**Consensus Rule:** An anomaly is only reported if at least 2 out of 3 methods agree. This reduces false positives significantly.

### Create `engine/anomaly_detector.py`

```python
# engine/anomaly_detector.py
"""
NAR8 AI — Anomaly Detection Engine

Uses three statistical methods to identify unusual sales patterns:
  1. Z-Score Analysis
  2. IQR (Interquartile Range) Analysis
  3. Rolling Average Percentage Deviation

Consensus rule: An anomaly is flagged only when ≥2 of 3 methods agree.
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
             c. Flags if ≥2 methods agree
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

            # ── Consensus rule: need ≥2 methods to agree ─────────────
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
```

### Phase 3 Test

```python
# tests/test_phase3.py
from data.powerbi_connector import PowerBIConnector
from engine.anomaly_detector import AnomalyDetector

def test_anomaly_detection():
    connector = PowerBIConnector()
    df = connector.fetch_weekly_sales()

    detector = AnomalyDetector()
    report = detector.detect(df)

    print(f"\n✅ Week analyzed: {report.week_analyzed}")
    print(f"   Total anomalies: {report.total_anomalies}")
    print(f"   High severity:   {report.high_severity_count}")
    print(f"   Medium severity: {report.medium_severity_count}")
    print(f"   Overall sales:   ${report.overall_week_sales:,.2f}")
    print(f"   WoW change:      {report.wow_change_pct:+.1f}%")
    print(f"\n   Top segment:    {report.top_segment}")
    print(f"   Bottom segment: {report.bottom_segment}")

    print(f"\n── Anomaly Details ──")
    for a in report.anomalies:
        print(f"  [{a.severity}] {a.description}")

    assert report.total_anomalies >= 1, "Should detect at least 1 anomaly in mock data"
    assert all(a.severity in ["HIGH", "MEDIUM", "LOW"] for a in report.anomalies)
    print("\n✅ All assertions passed.")

if __name__ == "__main__":
    test_anomaly_detection()
```

Run: `python tests/test_phase3.py`

---

## Phase 4 — LLM Narrative Generator

> **Goal:** Transform anomaly data into an executive-quality, structured business narrative.
> **What you learn:** LLM API integration, prompt engineering, structured JSON output, error handling.
> **Estimated time:** 3–4 hours

### What Prompt Engineering Means Here

Prompt engineering is the craft of writing instructions to an LLM that produce consistent, high-quality, predictable output. Bad prompt: "write about my sales data." Good prompt: gives the LLM a role, all necessary data, an exact output format, tone requirements, and length constraints. You are not asking the LLM to think freely — you are directing it like a precise tool.

Key principles used in this prompt:
- **Role assignment:** "You are a Senior Business Intelligence Analyst..." — this sets the writing style and expertise level
- **Structured output:** You specify the exact JSON schema and field names — this makes the output machine-readable
- **Data injection:** All anomaly numbers are embedded directly in the prompt — no hallucination possible
- **Tone constraints:** "never use filler phrases" — prevents fluffy corporate writing
- **Temperature:** Set to 0.4 (on a scale of 0–2) — lower means more focused and consistent

### Create `engine/llm_narrator.py`

```python
# engine/llm_narrator.py
"""
NAR8 AI — LLM Narrative Generator

Takes an AnomalyReport and generates a structured, JSON-format
business narrative using an LLM API (OpenAI or Anthropic).

The output JSON maps directly to the 5-slide PowerPoint structure:
  - executive_summary  → Slide 1 headline + KPI bar
  - slide_2_overview   → Performance overview slide
  - slide_3_anomalies  → Anomaly detail cards slide
  - slide_4_insights   → Strategic insights slide
  - slide_5_recs       → Recommendations slide
"""
import json
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

    # ── Prompt Builder ────────────────────────────────────────────────

    def _build_prompt(self, report: AnomalyReport) -> str:
        """
        Constructs the full prompt string.
        All data values are injected directly — no LLM guessing.
        """

        # Format anomaly list for the prompt
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
  An anomaly is flagged only when ≥2 of 3 methods agree — reducing false positives.

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
        "value": "{((report.overall_week_sales - report.avg_weekly_sales) / report.avg_weekly_sales * 100):+.1f}%",
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

    # ── LLM API Callers ───────────────────────────────────────────────

    def _call_openai(self, prompt: str) -> str:
        """Calls OpenAI Chat Completions API."""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Run: pip install openai")

        client = OpenAI(api_key=self.config.OPENAI_API_KEY)

        response = client.chat.completions.create(
            model=self.config.LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a business intelligence expert. "
                        "You always respond with valid JSON only. "
                        "Never include markdown, backticks, or any text outside the JSON object."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=self.config.LLM_TEMPERATURE,
            max_tokens=self.config.LLM_MAX_TOKENS,
            response_format={"type": "json_object"},  # Forces JSON mode in newer models
        )

        return response.choices[0].message.content

    def _call_anthropic(self, prompt: str) -> str:
        """Calls Anthropic Claude API."""
        try:
            import anthropic
        except ImportError:
            raise ImportError("Run: pip install anthropic")

        client = anthropic.Anthropic(api_key=self.config.ANTHROPIC_API_KEY)

        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=self.config.LLM_MAX_TOKENS,
            system=(
                "You are a business intelligence expert. "
                "You always respond with valid JSON only. "
                "Never include markdown, backticks, or any text outside the JSON object."
            ),
            messages=[{"role": "user", "content": prompt}],
        )

        return message.content[0].text

    # ── Response Parser ───────────────────────────────────────────────

    def _parse_response(self, raw: str) -> dict:
        """
        Cleans and parses the LLM's raw text response into a Python dict.
        Handles edge cases like markdown fences or extra whitespace.
        """
        raw = raw.strip()

        # Strip markdown code fences if present (model sometimes adds them)
        if raw.startswith("```"):
            lines = raw.split("\n")
            # Remove first line (```json or ```) and last line (```)
            lines = [l for l in lines if not l.strip().startswith("```")]
            raw = "\n".join(lines).strip()

        # Find the outermost JSON object
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON object found in LLM response")

        json_str = raw[start:end]

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Print first 500 chars to help debug
            print(f"⚠ JSON parse error: {e}")
            print(f"  Raw response preview: {json_str[:500]}")
            raise

    # ── Main Public Method ────────────────────────────────────────────

    def generate_narrative(self, report: AnomalyReport) -> dict:
        """
        Builds the prompt, calls the LLM, parses the JSON response.

        Args:
            report: AnomalyReport from the AnomalyDetector

        Returns:
            Structured dict with all slide content, ready for SlideBuilder
        """
        prompt = self._build_prompt(report)

        print(f"📡 Calling {self.config.LLM_PROVIDER.upper()} API ({self.config.LLM_MODEL})...")
        print(f"   Prompt length: {len(prompt)} characters")

        if self.config.LLM_PROVIDER == "anthropic":
            raw = self._call_anthropic(prompt)
        else:
            raw = self._call_openai(prompt)

        print(f"   Response length: {len(raw)} characters")

        narrative = self._parse_response(raw)
        print("✅ Narrative generated and parsed successfully")

        return narrative
```

### Phase 4 Test

```python
# tests/test_phase4.py
import json
from data.powerbi_connector import PowerBIConnector
from engine.anomaly_detector import AnomalyDetector
from engine.llm_narrator import LLMNarrator

def test_narrative_generation():
    # Get data and detect anomalies
    df = PowerBIConnector().fetch_weekly_sales()
    report = AnomalyDetector().detect(df)

    # Generate narrative
    narrator = LLMNarrator()
    narrative = narrator.generate_narrative(report)

    print("\n✅ Narrative generated successfully")
    print(f"\n── Executive Summary ──")
    print(f"  Headline:   {narrative['executive_summary']['headline']}")
    print(f"  Sentiment:  {narrative['executive_summary']['sentiment']}")
    print(f"  TL;DR:      {narrative['executive_summary']['tldr'][:120]}...")

    print(f"\n── Slides Present ──")
    for key in narrative:
        print(f"  ✓ {key}")

    # Verify structure
    required_keys = [
        "executive_summary", "slide_1_title", "slide_2_overview",
        "slide_3_anomalies", "slide_4_insights", "slide_5_recommendations"
    ]
    for key in required_keys:
        assert key in narrative, f"Missing key: {key}"

    print("\n✅ All structure assertions passed.")
    print("\nFull narrative JSON:")
    print(json.dumps(narrative, indent=2))

if __name__ == "__main__":
    test_narrative_generation()
```

Run: `python tests/test_phase4.py`

---

## Phase 5 — Chart Generator

> **Goal:** Create three data visualization charts as PNG images for embedding in slides.
> **What you learn:** Matplotlib, chart design principles, saving figures to disk.
> **Estimated time:** 2–3 hours

### Three Charts You Will Generate

**Chart 1 — Weekly Sales Trend Line:** Shows all 13 weeks of total sales as a line chart. Includes a 4-week rolling average as a dashed line. Highlights the current week with a shaded region. This gives the reader immediate context for whether this week is normal.

**Chart 2 — Category Sales Bar Chart:** Horizontal bars showing this week's sales per product category, with translucent overlay bars showing the historical average. Color-coded so anomalous categories stand out visually.

**Chart 3 — Region × Category Heatmap:** A grid where rows are product categories and columns are regions. Each cell shows the percentage deviation from historical average, colored from deep red (large drop) to deep green (large spike). This is the most technically interesting chart and the most visually striking.

### Create `output/chart_generator.py`

```python
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
    print(f"   ✓ Trend chart saved: {path}")
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
    print(f"   ✓ Category chart saved: {path}")
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
    print(f"   ✓ Heatmap saved: {path}")
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

    print("📈 Generating charts...")
    return {
        "trend":    create_trend_chart(df, charts_dir),
        "category": create_category_chart(df, charts_dir),
        "heatmap":  create_heatmap(df, charts_dir),
    }
```

---

## Phase 6 — Slide Deck Builder

> **Goal:** Assemble the complete PowerPoint presentation from narrative JSON and chart images.
> **What you learn:** python-pptx library, programmatic layout design, color and typography in code.
> **Estimated time:** 4–5 hours (most visual, most detailed phase)

### Key python-pptx Concepts

Before writing code, understand these concepts:

**Presentation** — The entire .pptx file object. You call `save()` on it at the end.

**Slide** — One page. Added with `prs.slides.add_slide(layout)`. You use the blank layout (index 6) so nothing is pre-placed.

**Shape** — Any element on a slide. Text boxes, images, and rectangles are all shapes. Every shape has a position (`left`, `top`) and size (`width`, `height`), all measured in `Inches()`.

**Inches** — The unit system. `Inches(1.5)` means 1.5 inches from the edge. A 16:9 widescreen slide is 13.33 inches wide × 7.5 inches tall.

**RGB Color** — Colors are specified as `RGBColor(0x1E, 0x3A, 0x5F)` using the red, green, blue values in hex.

**TextFrame** — Inside a text box. Has paragraphs, each with runs. A run is a piece of text with its own formatting (bold, size, color).

### Create `output/slide_builder.py`

```python
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
        _add_text(slide, "From raw data to boardroom narrative — automatically.",
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
        headline = exec_sum.get("headline", f"Weekly Sales Report — {report.week_analyzed}")
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
            "POSITIVE": "▲", "NEGATIVE": "▼", "MIXED": "◆", "NEUTRAL": "●"
        }.get(sentiment, "●")
        _add_text(slide, f"{sentiment_emoji}  {headline}",
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
                arrow = "▲" if direction == "UP" else ("▼" if direction == "DOWN" else "")
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
                    "segment":  f"{a.category} — {a.region}",
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
            direction_arrow = "▲" if card.get("direction") == "SPIKE" else "▼"
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
            _add_text(slide, "💡 Hypothesis:",
                      0.48, card_y + 0.90, 1.5, 0.35,
                      size=9, bold=True, color=CLR["navy"])
            _add_text(slide, card.get("hypothesis", ""),
                      1.95, card_y + 0.90, 5.7, 0.35,
                      size=9, italic=True, color=CLR["slate"])

            # Action label + text
            _add_text(slide, "→ Action:",
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
            _add_text(slide, "👁  WATCH NEXT WEEK",
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
                          f"Generated by NAR8 AI — {report.week_analyzed}")

        # Column 1: Immediate actions
        _add_rect(slide, 0.25, 1.05, 6.15, 0.52, CLR["blue"])
        _add_text(slide, "✅  Act This Week",
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
        _add_text(slide, "📊  Monitor Next Week",
                  7.05, 1.1, 5.8, 0.42,
                  size=13, bold=True, color=CLR["white"])

        monitors = s5.get("monitor", [])
        monitor_y = 1.65
        for item in monitors[:3]:
            _add_rect(slide, 6.85, monitor_y, 6.2, 0.82, CLR["light_orange"], CLR["light_gray"])
            _add_text(slide, "◎",
                      7.0, monitor_y + 0.12, 0.4, 0.6,
                      size=14, color=CLR["orange"])
            _add_text(slide, item,
                      7.35, monitor_y + 0.1, 5.55, 0.65,
                      size=10, color=CLR["dark_text"], word_wrap=True)
            monitor_y += 0.92

        # Closing statement banner
        closing = s5.get("closing", "NAR8 AI — Automated intelligence, delivered weekly.")
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
        print(f"✅ Slide deck saved: {full_path}")
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
    print("📋 Building slide deck...")
    builder = SlideBuilder()
    builder.build_title_slide(narrative, report)
    builder.build_overview_slide(narrative, report, charts)
    builder.build_anomalies_slide(narrative, report, charts)
    builder.build_insights_slide(narrative, report, charts)
    builder.build_recommendations_slide(narrative, report)

    return builder.save(save_dir)
```

---

## Phase 7 — Pipeline Orchestrator

> **Goal:** Wire all modules together into a clean, callable pipeline function.
> **What you learn:** Separation of concerns, orchestration patterns, CLI design.
> **Estimated time:** 30–45 minutes

### Create `main.py`

```python
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
    [1] Data Fetch       → PowerBIConnector
    [2] Anomaly Detection → AnomalyDetector
    [3] Narrative Gen    → LLMNarrator
    [4] Deck Build       → SlideBuilder + ChartGenerator
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
        # ── Validate config ───────────────────────────────────────────
        warnings = Config.validate()
        for w in warnings:
            log(f"⚠  {w}")

        log("\n" + "═" * 62)
        log("  NAR8 AI — Automated Data Storytelling Pipeline")
        log("═" * 62)

        # ── Stage 1: Fetch Data ───────────────────────────────────────
        log("\n[1/4] 📡 Fetching sales data...")
        connector = PowerBIConnector()
        df = connector.fetch_weekly_sales(weeks=weeks or Config.WEEKS_OF_DATA)
        result["df"] = df
        log(f"      ✓ {len(df)} rows | {df['week_start_date'].nunique()} weeks")
        log(f"        Categories: {', '.join(df['category'].unique())}")
        log(f"        Regions:    {', '.join(df['region'].unique())}")

        # ── Stage 2: Detect Anomalies ─────────────────────────────────
        log("\n[2/4] 🔍 Running anomaly detection engine...")
        detector = AnomalyDetector(
            z_threshold=z_threshold or Config.Z_SCORE_THRESHOLD,
            pct_threshold=pct_threshold or Config.PCT_CHANGE_THRESHOLD,
            lookback_weeks=lookback_weeks or Config.LOOKBACK_WEEKS,
        )
        report = detector.detect(df)
        result["report"] = report
        log(f"      ✓ Week: {report.week_analyzed}")
        log(f"        Anomalies: {report.total_anomalies} total "
            f"({report.high_severity_count} HIGH, "
            f"{report.medium_severity_count} MEDIUM, "
            f"{report.low_severity_count} LOW)")
        log(f"        WoW Change: {report.wow_change_pct:+.1f}%")
        if report.anomalies:
            log(f"        Top Anomaly: {report.anomalies[0].description[:80]}...")

        # ── Stage 3: Generate Narrative ───────────────────────────────
        log("\n[3/4] 🤖 Generating AI narrative...")
        narrator = LLMNarrator()
        narrative = narrator.generate_narrative(report)
        result["narrative"] = narrative
        headline = narrative.get("executive_summary", {}).get("headline", "N/A")
        log(f"      ✓ Headline: \"{headline}\"")

        # ── Stage 4: Build Slide Deck ─────────────────────────────────
        log("\n[4/4] 📊 Building PowerPoint slide deck...")
        save_dir = output_dir or Config.OUTPUT_DIR
        deck_path = build_deck(narrative, report, df, save_dir)
        result["deck_path"] = deck_path

        # ── Done ──────────────────────────────────────────────────────
        duration = round(time.time() - start_time, 1)
        result["duration_s"] = duration
        result["success"] = True

        log(f"\n{'═' * 62}")
        log(f"  ✅ NAR8 AI pipeline complete in {duration}s")
        log(f"  📄 Deck: {deck_path}")
        log(f"{'═' * 62}\n")

    except Exception as e:
        result["error"] = str(e)
        result["duration_s"] = round(time.time() - start_time, 1)
        log(f"\n❌ Pipeline failed: {e}")
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
```

---

## Phase 8 — Streamlit Web Dashboard

> **Goal:** Build the web interface that ties everything together for the user.
> **What you learn:** Streamlit components, session state, real-time UI updates, file downloads.
> **Estimated time:** 3–4 hours

### Create `ui/dashboard.py`

```python
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

            styled = anom_df.style.applymap(style_severity, subset=["Severity"])
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
                        st.image(fpath, use_column_width=True)
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

        # Tech stack display
        st.markdown("### 🛠️ Technology Stack")
        tech_cols = st.columns(5)
        techs = [
            ("🐍", "Python 3.11"),
            ("📊", "Power BI API"),
            ("🔬", "NumPy + SciPy"),
            ("🤖", "OpenAI / Claude"),
            ("📑", "python-pptx"),
        ]
        for col, (icon, name) in zip(tech_cols, techs):
            with col:
                st.markdown(f"**{icon} {name}**")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            "<center><i>Click 'Run Weekly Analysis' above to start the pipeline.</i></center>",
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
```

---

## Phase 9 — Branding, Polish & GitHub Setup

> **Goal:** Add the finishing touches that make this look like a real product.
> **Time estimate:** 1 day

### 9.1 Create a NAR8 AI Logo

You have two options:

**Option A (quickest):** Go to https://canva.com, create a free account, choose a 500×500px blank canvas, type "NAR8 AI" in a bold font like Montserrat or Raleway, use white text on a `#1E3A5F` navy background, add a small chart icon, download as PNG. Save as `assets/nar8_logo.png`.

**Option B:** Use https://looka.com or https://brandmark.io for a quick AI-generated logo using the name "NAR8 AI."

### 9.2 Write the README.md

```markdown
# 📊 NAR8 AI — Automated Data Storytelling

> From raw data to boardroom narrative — automatically.

NAR8 AI is an end-to-end Python pipeline that connects to Microsoft Power BI's
REST API, detects weekly sales anomalies using multi-method statistical analysis,
generates an executive narrative via a Large Language Model, and autonomously
produces a formatted PowerPoint slide deck.

---

## 🎯 What It Does

1. Fetches 13 weeks of sales data from Power BI REST API (or mock data)
2. Detects anomalies using Z-score, IQR, and rolling average deviation
3. Sends findings to GPT-4o-mini with a precision-engineered prompt
4. Receives a structured JSON business narrative
5. Generates 3 Matplotlib data visualizations
6. Assembles a branded 5-slide PowerPoint presentation
7. Delivers everything via a Streamlit web dashboard

---

## 🖥️ Demo Screenshot

[Add screenshot here]

---

## 🛠️ Tech Stack

`Python 3.11` · `Power BI REST API` · `OAuth 2.0` · `OpenAI GPT-4o-mini` ·
`Pandas` · `NumPy` · `SciPy` · `Matplotlib` · `python-pptx` · `Streamlit` · `MSAL`

---

## 🚀 Quick Start

```bash
git clone https://github.com/yourusername/nar8-ai.git
cd nar8-ai
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # Add your API keys
streamlit run ui/dashboard.py
```

---

## 📁 Project Structure

```
nar8-ai/
├── config/settings.py          # Central configuration
├── data/powerbi_connector.py   # Power BI REST API + mock data
├── engine/anomaly_detector.py  # Statistical anomaly detection
├── engine/llm_narrator.py      # LLM narrative generation
├── output/chart_generator.py   # Matplotlib chart creation
├── output/slide_builder.py     # PowerPoint assembly
├── ui/dashboard.py             # Streamlit web interface
└── main.py                     # Pipeline orchestrator
```

---

## ⚙️ Configuration

Copy `.env.example` to `.env` and fill in:

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `LLM_MODEL` | e.g. `gpt-4o-mini` |
| `USE_MOCK_DATA` | `true` for demo, `false` for real Power BI |
| `POWERBI_CLIENT_ID` | Azure app client ID |
| `POWERBI_TENANT_ID` | Azure tenant ID |

---

## 📄 License

MIT License — free for personal and academic use.
```

### 9.3 Push to GitHub

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit — NAR8 AI v1.0.0"

# Create a repo on github.com named 'nar8-ai', then:
git remote add origin https://github.com/yourusername/nar8-ai.git
git branch -M main
git push -u origin main
```

---

## Testing Checklist

Run these in order after completing each phase. Every item must pass before moving to the next phase.

```bash
# Phase 1 — Config
python tests/test_phase1.py
# Expected: Config values printed, no errors

# Phase 2 — Data Layer
python tests/test_phase2.py
# Expected: 156 rows, 13 weeks, assertion passed

# Phase 3 — Anomaly Detection
python tests/test_phase3.py
# Expected: ≥1 anomaly found, HIGH severity, description printed

# Phase 4 — LLM Narrative
python tests/test_phase4.py
# Expected: JSON narrative printed, all 6 keys present

# Full Pipeline (CLI)
python main.py
# Expected: All 4 stages complete, .pptx file created

# Streamlit UI
streamlit run ui/dashboard.py
# Expected: Browser opens at localhost:8501, run button works, download available
```

---

## Recommended Timeline

| Day | Task | Phase |
|---|---|---|
| Day 1 | Python setup, VS Code, virtual env, packages | Setup |
| Day 1 | Azure app registration, API keys, .env | Setup |
| Day 2 | Config module, folder scaffold, Phase 1 test | Phase 1 |
| Day 2–3 | Mock data generator, Power BI connector | Phase 2 |
| Day 3–4 | Anomaly detector (all 3 methods), Phase 3 test | Phase 3 |
| Day 4–5 | LLM narrator, prompt engineering, Phase 4 test | Phase 4 |
| Day 5–6 | All 3 charts (trend, bar, heatmap) | Phase 5 |
| Day 6–8 | All 5 slides in python-pptx | Phase 6 |
| Day 8 | main.py orchestrator, CLI test | Phase 7 |
| Day 9 | Streamlit dashboard | Phase 8 |
| Day 10 | Branding, README, GitHub push, demo prep | Phase 9 |

---

## Resume & LinkedIn Write-Up

### Resume Project Entry

**NAR8 AI — Automated Data Storytelling via Generative AI** | Python · Power BI REST API · OpenAI · Streamlit

- Designed and built an end-to-end generative AI pipeline integrating Power BI REST API (OAuth 2.0) with multi-method statistical anomaly detection to autonomously analyze 13-week sales semantic model data
- Implemented three-method consensus anomaly detection (Z-score, IQR, rolling average) with configurable sensitivity thresholds, detecting segment deviations as low as ±30% from historical baseline
- Engineered structured JSON-output LLM prompts (GPT-4o-mini) producing consistent executive-quality business narratives mapped directly to a 5-slide presentation schema
- Automated PowerPoint generation using python-pptx, embedding dynamically generated Matplotlib visualizations (trend line, category breakdown, deviation heatmap)
- Deployed interactive Streamlit dashboard with real-time pipeline progress, anomaly severity tables, chart previews, and one-click .pptx download

### Skills for LinkedIn

`Python` · `Power BI REST API` · `OAuth 2.0` · `Azure AD` · `Generative AI` · `Prompt Engineering` · `OpenAI API` · `Statistical Analysis` · `Anomaly Detection` · `Pandas` · `NumPy` · `SciPy` · `Matplotlib` · `python-pptx` · `Streamlit` · `Data Visualization` · `Automation` · `REST APIs`

---

## Troubleshooting Guide

**`ModuleNotFoundError` on any import**
Your virtual environment is not activated. Run `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux) before running any Python command.

**`openai.AuthenticationError`**
Your `OPENAI_API_KEY` is missing or wrong in `.env`. Make sure the file is in the project root (same folder as `main.py`) and the key starts with `sk-`.

**LLM response is not valid JSON**
The model occasionally adds text around the JSON. The `_parse_response()` method handles most cases. If it still fails, lower `LLM_TEMPERATURE` to `0.2` in `config/settings.py` for more deterministic output.

**Charts not appearing in slides**
Check that `output/slides/charts/` exists and contains `.png` files after the chart generation step. The `_add_image()` helper will show a placeholder if the file is missing rather than crashing.

**`python-pptx` text is overflowing or misaligned**
Positions use `Inches()`. The slide canvas is 13.33 × 7.5 inches. Sketch each slide on paper with measurements before coding. Small adjustments to `left`, `top`, `width`, and `height` values in `slide_builder.py` fix alignment issues.

**Power BI API returns 401 Unauthorized**
The Azure app does not have the correct permissions or admin consent was not granted. Revisit Section 6.6 step-by-step. The most common cause is forgetting to click "Grant admin consent" after adding API permissions.

**Streamlit button does nothing**
Make sure you are running `streamlit run ui/dashboard.py` from the `nar8-ai/` project root, not from inside the `ui/` subfolder. The `sys.path` fix in `dashboard.py` handles most cases, but the working directory must be the project root.

---

*NAR8 AI — Built as a data visualization college project. The architecture mirrors real enterprise BI automation pipelines used by consulting firms and BI teams worldwide.*
