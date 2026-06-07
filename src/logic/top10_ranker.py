import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================
BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = PROCESSED_DIR
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DAILY FLOW FILE
# ============================================================
def load_flow_data() -> pd.DataFrame:
    file_path = PROCESSED_DIR / "institutional_flow_daily.csv"
    if not file_path.exists():
        raise FileNotFoundError("institutional_flow_daily.csv not found")
    return pd.read_csv(file_path)


# ============================================================
# SCORE & RANK
# ============================================================
def rank_top_stocks(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    df = df.copy()

    # Money Flow Score already exists (flow_score)
    # Sort by:
    # 1) flow_score (desc)
    # 2) volume (desc) as tiebreaker
    df.sort_values(
        by=["flow_score", "volume"],
        ascending=[False, False],
        inplace=True
    )

    top_df = df.head(top_n).reset_index(drop=True)

    # Add rank column
    top_df.insert(0, "rank", range(1, len(top_df) + 1))

    return top_df


# ============================================================
# MAIN RUNNER
# ============================================================
def run():
    df = load_flow_data()
    top10 = rank_top_stocks(df, top_n=10)

    output_file = OUTPUT_DIR / "top10_institutional_picks.csv"
    top10.to_csv(output_file, index=False)

    print(f"Top 10 Institutional Picks saved → {output_file}")
    print(top10[["rank", "symbol", "flow_signal", "flow_score"]])


if __name__ == "__main__":
    run()
