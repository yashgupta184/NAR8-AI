# NAR8 AI - Current Implementation Details

## 1. Project Overview
NAR8 AI is an automated weekly sales intelligence system. It acts as an AI-powered data analyst that extracts sales data, detects statistical anomalies, generates an executive narrative, and creates a boardroom-ready PowerPoint presentation, all accessible via a Streamlit web interface.

## 2. Technology Stack
- **Language**: Python 3.11+
- **Data Layer**: Pandas, Numpy, Power BI REST API (or Mock Data Generator)
- **Engine Layer**: SciPy (Stats), OpenAI GPT-4o-mini / Anthropic Claude
- **Output Layer**: Matplotlib, python-pptx, Pillow
- **UI Layer**: Streamlit
- **Auth & Config**: MSAL, python-dotenv

## 3. System Architecture
The application uses a modular, sequential pipeline architecture:
1. **Data Connector**: Authenticates with Power BI (OAuth 2.0) or generates mock data, returning a standard Pandas DataFrame.
2. **Anomaly Engine**: Processes 13 weeks of data using a three-method consensus (Z-Score, IQR, Rolling Average) to flag significant variations.
3. **LLM Narrator**: Compiles findings and injects them into an engineered prompt for an LLM to generate a structured JSON narrative.
4. **Visualizer**: Uses Matplotlib to generate PNG charts highlighting the current week vs. baseline.
5. **Slide Builder**: Integrates the JSON narrative and charts into a 5-slide PowerPoint deck using `python-pptx`.
6. **Orchestrator & UI**: `main.py` binds the modules, while Streamlit provides a user-friendly trigger and download interface.

## 4. Implementation Phases
### Phase 1: Foundation
- Scaffolding the directory structure (`config/`, `data/`, `engine/`, `output/`, `ui/`, `tests/`).
- Centralizing environment variables and constants in `config/settings.py`.

### Phase 2: Data Abstraction
- Building `mock_sales_data.py` for local testing with planted anomalies.
- Implementing `powerbi_connector.py` for Azure AD client credentials authentication and DAX query execution.

### Phase 3: Statistical Anomaly Detection
- Implementing `AnomalyDetector` class.
- Z-Score Analysis (Threshold ±2.0).
- IQR Fence detection.
- Rolling Average Percentage Deviation (±30%).
- Consensus rule applied: Requires 2/3 methods to trigger.

### Phase 4: Generative AI Narrative
- Structured prompt engineering enforcing strict JSON output.
- Dynamic data injection to eliminate hallucinations.
- LLM API integration with robust error handling.

### Phase 5 & 6: Asset Generation
- `chart_generator.py` for exporting Pandas plots to PNG.
- `slide_builder.py` mapping the LLM JSON fields precisely to PowerPoint slide layouts.

### Phase 7 & 8: Pipeline & UI
- Orchestration script to run sequentially.
- Streamlit web interface for one-click execution and file download.

Activate the environment:
.\venv_313\Scripts\Activate.ps1
