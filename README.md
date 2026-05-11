# ⚡ NAR8 AI 
**Automated Intelligence & Data Storytelling Platform**

![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Power BI](https://img.shields.io/badge/PowerBI-F2C811?logo=powerbi&logoColor=black)
![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?logo=google&logoColor=white)

NAR8 AI is an enterprise-grade automated data storytelling platform. It bridges the gap between raw quantitative data and strategic business decisions by ingesting multi-region sales data, identifying statistical anomalies using consensus algorithms, and leveraging Generative AI to autonomously synthesize boardroom-ready PowerPoint narratives.

---

## 🌟 Key Features

1. **Enterprise Data Ingestion**
   - **Power BI REST API Integration**: Connects securely via Microsoft Azure OAuth 2.0 to fetch live, multidimensional enterprise datasets.
   - **Custom CSV Uploads**: Features a drag-and-drop CSV uploader for ad-hoc analysis, instantly overriding the Power BI connection.

2. **Consensus Anomaly Engine**
   - Uses a tri-method consensus algorithm (Z-Score Analysis, Interquartile Range, and Rolling % Deviation) to identify only high-fidelity statistical deviations and reduce executive noise.

3. **Generative AI Narratives**
   - Integrates with Google Gemini 2.5 Flash (or OpenAI/Anthropic) to transform mathematical anomalies into actionable, strategic business narratives formatted as a structured JSON payload.

4. **Automated Presentation Rendering**
   - Leverages `python-pptx` to dynamically assemble a fully branded, 5-slide executive presentation containing dynamic KPI cards and precise Matplotlib visualizations.

5. **Premium Web Dashboard**
   - Built on Streamlit with a highly refined **Sleek Dark Mode**, glassmorphism styling, and custom Google Typography (Outfit).
   - Features fully interactive `plotly` data visualizations (Trend Lines, Category Bars, Heatmaps).

---

## 🏗️ Architecture

The pipeline is entirely modular and decoupled:
- `data/`: Ingestion layer (Power BI OAuth or Mock Data simulation).
- `engine/`: Processing layer (Statistical Anomaly Detector + LLM Narrator).
- `output/`: Rendering layer (Slide Builder + Static Chart Generator).
- `ui/`: Interactive frontend layer (Streamlit Dashboard).
- `main.py`: The central orchestrator that links all components.

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.13+ installed.
```bash
git clone https://github.com/yashgupta184/NAR8-AI.git
cd NAR8-AI
python -m venv venv
```

**Activate Environment:**
- Windows: `.\venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory (you can copy `.env.example`).
```env
# ── LLM Configuration ──
GEMINI_API_KEY=your_gemini_key_here
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.5-flash

# ── Power BI Configuration ──
USE_MOCK_DATA=true  # Set to 'false' to enable live Power BI data
# POWERBI_CLIENT_ID=...
```

*(Note: If deploying to Streamlit Community Cloud, enter these variables in the **Streamlit Secrets** using TOML format instead of `.env`)*

---

## 💻 Usage

### Launch the Web Dashboard (Recommended)
This launches the premium interactive UI.
```bash
streamlit run ui/dashboard.py
```

### Run via Command Line
You can run the entire pipeline headless and generate a presentation directly.
```bash
python main.py
```

*Optional CLI arguments:*
- `--weeks 12`: Analyze a specific number of weeks.
- `--z-threshold 2.5`: Override the Z-score sensitivity.

---

## 🛠️ Technology Stack
- **Backend**: Python 3.13, Pandas, NumPy, SciPy
- **Visualizations**: Plotly (Interactive), Matplotlib (Static/PPTX)
- **AI / LLM**: Google GenAI SDK
- **Frontend**: Streamlit + Custom CSS
- **Presentation**: `python-pptx`

---
*Developed for modern enterprise intelligence.*
