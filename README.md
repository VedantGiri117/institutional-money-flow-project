# Institutional Money Flow Tracker

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge\&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge\&logo=streamlit)
![Google Gemini](https://img.shields.io/badge/Google-Gemini_AI-4285F4?style=for-the-badge\&logo=google)
![NSE BHARAT](https://img.shields.io/badge/Data_Source-NSE-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)

---

# Institutional Money Flow Tracker

##Project output screenshot

<img width="1452" height="926" alt="image" src="https://github.com/user-attachments/assets/cde61606-5904-45c0-8043-db5521ce4d45" />


A production-grade financial analytics platform that 
* transforms raw NSE market data into actionable institutional trading intelligence.
* The system automatically ingests NSE Bhavcopy reports, 
* calculates institutional money flow signals, 
* ranks high-conviction investment opportunities,
* generates AI-powered market commentary using Google Gemini,
* delivers results through an interactive Streamlit dashboard designed for analysts, traders, and investment researchers.

By combining quantitative ranking models with large language model (LLM) synthesis, the platform enables rapid identification of accumulation patterns, sector rotation themes, and institutional participation trends across Indian equity markets.

---

## Key Features

### Automated NSE Data Ingestion

* Fetches daily NSE Bhavcopy reports automatically.
* Maintains historical raw market datasets.
* Supports repeatable and auditable data pipelines.

### Institutional Money Flow Analytics

* Processes daily market activity.
* Calculates proprietary money flow metrics.
* Detects accumulation and participation signals.
* Tracks institutional trading behavior.

### Top 10 Opportunity Ranking Engine

* Ranks securities using flow-based scoring.
* Implements deterministic multi-level sorting.
* Generates a ranked watchlist of institutional opportunities.

### Google Gemini AI Market Commentary

* Converts quantitative outputs into narrative insights.
* Explains sector trends and market positioning.
* Generates institutional-style research commentary.

### Interactive Analyst Dashboard

* Wide-layout Streamlit interface.
* High-density data visualization.
* Professional analyst workflow.
* Integrated AI commentary panel.

---

# System Architecture

```text
NSE Bhavcopy Data
        │
        ▼
Data Extraction
        │
        ▼
Institutional Flow Processing
        │
        ▼
Ranking Engine
        │
        ▼
Top 10 Institutional Picks
        │
        ▼
Google Gemini Analysis
        │
        ▼
AI Investment Commentary
        │
        ▼
Streamlit Dashboard
```

---

# End-to-End Processing Pipeline

The application operates through six distinct engineering phases.

---

## Phase 1 & 2 — Data Extraction & Ingestion

### Script

```text
src/nse/bhavcopy_fetcher.py
```

### Purpose

Automates retrieval of daily NSE Bhavcopy reports and stores them within the raw data layer.

### Output Example

```text
data/raw/bhavcopy/
└── bhavcopy_2026-02-05.csv
```

### Responsibilities

* Connects to NSE data sources
* Downloads daily market reports
* Creates standardized raw datasets
* Preserves historical market records

---

## Phase 3 & 4 — Institutional Flow Processing & Ranking

### Scripts

```text
src/logic/institutional_flow.py
src/logic/top10_ranker.py
```

### Purpose

Transforms processed market metrics into a ranked list of institutional investment opportunities.

### Ranking Workflow

#### Step 1

Load:

```text
data/processed/institutional_flow_daily.csv
```

#### Step 2

Execute deterministic sorting logic:

| Priority  | Field      | Direction  |
| --------- | ---------- | ---------- |
| Primary   | flow_score | Descending |
| Secondary | volume     | Descending |

This ensures consistent ranking behavior even when multiple securities have identical flow scores.

#### Step 3

Select the highest-ranked:

```text
Top 10 Securities
```

#### Step 4

Generate a sequential ranking column:

```text
rank = 1 → 10
```

#### Step 5

Export results:

```text
data/processed/top10_institutional_picks.csv
```

### Example Metrics

The ranking engine frequently surfaces securities such as:

* TATASTEEL
* PFC
* CANBK
* SBIN

alongside signals like:

```text
ACCUMULATION
```

and multi-million share trading volumes.

---

## Phase 5 — LLM Financial Analysis

### Script

```text
src/ai/gemini_summary.py
```

### Purpose

Generate institutional-grade market commentary using Google Gemini.

### Input

```text
top10_institutional_picks.csv
institutional_flow_daily.csv
```

### Output

```text
data/processed/ai_investment_summary.txt
```

### AI Commentary Themes

The AI engine synthesizes themes such as:

* Broad-based Interest with PSU Tilt
* Institutional Accumulation Trends
* Perceived Value Catalysts
* Sector Rotation Dynamics
* Portfolio Rebalancing Activity
* Macro-Economic Tailwinds

This bridges quantitative screening with qualitative market interpretation.

---

## Phase 6 — Interactive Analyst Dashboard

### Script

```text
src/ui/app.py
```

### Purpose

Provide an interactive visualization layer for analysts and investors.

### UI Configuration

* Streamlit
* Wide-screen layout
* Dark-themed interface
* High-density financial data presentation

---

### Data Validation Layer

Before rendering, the application verifies:

```text
data/processed/top10_institutional_picks.csv
```

If unavailable:

```text
Top 10 data not found. Run Phase 4 first.
```

Application execution stops immediately to prevent invalid reporting.

---

### Institutional Ranking Table

The dashboard renders a structured dataframe using the exact schema:

| Column      |
| ----------- |
| rank        |
| symbol      |
| flow_signal |
| flow_score  |
| volume      |

---

### AI Commentary Panel

The dashboard checks for:

```text
data/processed/ai_investment_summary.txt
```

If present:

* Displays AI-generated institutional commentary
* Shows analyst-ready market interpretation
* Provides approximately 350px of dedicated viewing space

If absent:

```text
AI summary not generated yet. Run Phase 5 (AI) first.
```

---

# 📂 Project Structure

```text
.
├── configs/
│   └── ai_config.json
│
├── data/
│   ├── raw/
│   │   └── bhavcopy/
│   │
│   └── processed/
│       ├── ai_investment_summary.txt
│       ├── institutional_flow_daily.csv
│       └── top10_institutional_picks.csv
│
├── src/
│   ├── ai/
│   │   └── gemini_summary.py
│   │
│   ├── logic/
│   │   ├── institutional_flow.py
│   │   └── top10_ranker.py
│   │
│   ├── nse/
│   │   └── bhavcopy_fetcher.py
│   │
│   └── ui/
│       └── app.py
│
├── environment.yml
├── health_check.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## Prerequisites

* Python 3.13+
* Conda (Recommended)
* Git
* Internet Connection
* Google Gemini API Access

---

## Option 1 — Conda Environment

```bash
git clone https://github.com/your-username/institutional-money-flow-tracker.git

cd institutional-money-flow-tracker

conda env create -f environment.yml

conda activate institutional-money-flow-tracker
```

---

## Option 2 — requirements.txt

```bash
git clone https://github.com/your-username/institutional-money-flow-tracker.git

cd institutional-money-flow-tracker

python -m venv venv
```

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🩺 Health Check

Verify project configuration:

```bash
python health_check.py
```

This confirms that required dependencies and runtime configuration are correctly installed.

---

# ▶️ Usage

## Step 1 — Fetch NSE Bhavcopy Data

```bash
python src/nse/bhavcopy_fetcher.py
```

---

## Step 2 — Generate Institutional Flow Metrics

```bash
python src/logic/institutional_flow.py
```

---

## Step 3 — Generate Top 10 Institutional Picks

```bash
python src/logic/top10_ranker.py
```

Output:

```text
data/processed/top10_institutional_picks.csv
```

---

## Step 4 — Generate AI Market Commentary

```bash
python src/ai/gemini_summary.py
```

Output:

```text
data/processed/ai_investment_summary.txt
```

---

## Step 5 — Launch Dashboard

```bash
streamlit run src/ui/app.py
```

---

## Step 6 — Open Browser

```text
http://localhost:8501
```

---

# 📊 Generated Outputs

| File                          | Description                      |
| ----------------------------- | -------------------------------- |
| institutional_flow_daily.csv  | Daily institutional flow metrics |
| top10_institutional_picks.csv | Ranked investment opportunities  |
| ai_investment_summary.txt     | AI-generated market commentary   |

---

# 🛠 Technology Stack

### Backend

* Python 3.13
* Pandas
* Pathlib

### Data Engineering

* NSE Bhavcopy Processing
* CSV-Based Data Pipelines

### Artificial Intelligence

* Google Gemini API
* LLM-Powered Financial Commentary

### Frontend

* Streamlit
* Interactive Data Tables
* Responsive Wide-Screen Layout

### Environment & Deployment

* Conda
* Virtual Environments
* requirements.txt Dependency Management

---

# 🎯 Use Cases

* Institutional Flow Monitoring
* Equity Screening
* Quantitative Trading Research
* Market Sentiment Analysis
* AI-Assisted Financial Reporting
* Portfolio Idea Generation
* Sector Rotation Tracking

---

# 🔮 Future Enhancements

* Real-Time NSE Streaming
* Historical Trend Charts
* Portfolio Monitoring
* Email Alerting System
* Telegram Notifications
* Machine Learning Ranking Models
* Multi-Factor Scoring Engine
* Cloud Deployment Support

---

# 📄 License

Distributed under the MIT License.

---

# 👨‍💻 Author

Developed as a full-stack financial analytics platform combining data engineering, quantitative ranking systems, artificial intelligence, and interactive visualization to support institutional-style market research workflows.
