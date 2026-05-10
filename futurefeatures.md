# NAR8 AI - Future Features & Scalability Roadmap

As NAR8 AI evolves from an MVP into a production-grade enterprise product, the architecture must scale to support greater automation, deeper insights, and seamless distribution. 

## 1. Automated Distribution (Email Integration)
**Objective**: Eliminate the need for users to manually click "download" and send emails.
- **Implementation**: Integrate SMTP, SendGrid API, or Microsoft Graph API.
- **Workflow**: A cron job (or Airflow/Celery task) triggers the pipeline every Monday at 6:00 AM. Upon successful `.pptx` generation, the system constructs an HTML email containing the Executive Summary (from the LLM) and attaches the presentation, sending it directly to stakeholders.

## 2. Advanced Predictive AI & Root Cause Analysis
**Objective**: Move from descriptive analytics ("what happened") to predictive and prescriptive analytics ("why it happened and what will happen").
- **Implementation**: 
  - Integrate a specialized forecasting model (e.g., Prophet, ARIMA, or advanced ML models) to project next week's sales.
  - Implement an Agentic Workflow (using LangChain/LlamaIndex) where the LLM can trigger web searches or query internal databases to find *why* an anomaly occurred (e.g., correlating a drop in sales with a major news event or supply chain disruption).

## 3. Persistent Database & State Management
**Objective**: Track anomalies over time and learn from user feedback.
- **Implementation**: Introduce PostgreSQL (via SQLAlchemy/Prisma).
- **Workflow**: Store all generated reports and flagged anomalies. Allow users to mark anomalies as "False Positives" in the UI, training a feedback loop that adjusts the Z-score and IQR thresholds dynamically per product category.

## 4. Multi-Tenant SaaS Architecture
**Objective**: Allow multiple departments or external companies to use NAR8 AI with isolated data.
- **Implementation**: 
  - Transition from hardcoded `.env` credentials to a database-backed credential manager.
  - Implement User Authentication (Auth0 or Azure AD SSO) in Streamlit or migrate to a full Next.js/FastAPI stack.
  - Ensure Row-Level Security (RLS) so users only see narratives for their authorized datasets.

## 5. Interactive Dashboard Drill-Downs
**Objective**: Let users explore the numbers behind the narrative.
- **Implementation**: Embed interactive Plotly or Power BI components directly into the UI. If an executive reads a narrative about a "Drop in South Region Apparel," they can click it to see the raw transaction data immediately.

## 6. Dynamic DAX Query Generation
**Objective**: Allow users to ask natural language questions about custom timeframes.
- **Implementation**: Use an LLM as a Text-to-SQL/DAX translator. Instead of a hardcoded weekly query, users could type: "Generate a narrative for Q3 Electronics margins," and the system generates the DAX, fetches the data, and runs the pipeline.