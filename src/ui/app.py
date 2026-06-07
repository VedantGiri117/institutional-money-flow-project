import streamlit as st
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"

st.set_page_config(page_title="Institutional Money Flow Tracker", layout="wide")

st.title("Institutional Money Flow Tracker")

# ============================================================
# LOAD DATA
# ============================================================
top10_file = DATA_DIR / "top10_institutional_picks.csv"
summary_file = DATA_DIR / "ai_investment_summary.txt"

if not top10_file.exists():
    st.error("Top 10 data not found. Run Phase 4 first.")
    st.stop()

df = pd.read_csv(top10_file)

# ============================================================
# TOP 10 TABLE
# ============================================================
st.subheader(" Top 10 Institutional Picks (Today)")
st.dataframe(
    df[["rank", "symbol", "flow_signal", "flow_score", "volume"]],
    use_container_width=True
)

# ============================================================
# AI SUMMARY
# ============================================================
st.subheader("    AI Investment Summary")

if summary_file.exists():
    with open(summary_file, "r") as f:
        summary_text = f.read()
    st.text_area("Summary", summary_text, height=350)
else:
    st.warning("AI summary not generated yet. Run Phase 5 (AI) first.")
