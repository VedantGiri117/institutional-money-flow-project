import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================
BASE_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD CLEAN DATA
# ============================================================
def load_processed_data() -> pd.DataFrame:
    file_path = PROCESSED_DIR / "bhavcopy_processed.csv"
    if not file_path.exists():
        raise FileNotFoundError("Processed bhavcopy not found")
    return pd.read_csv(file_path)


# ============================================================
# INSTITUTIONAL FLOW LOGIC
# ============================================================
def detect_institutional_flow(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    volume_threshold = df["volume"].median() * 1.5

    def classify(row):
        if row["volume"] >= volume_threshold and abs(row["price_change_pct"]) <= 1.5:
            if row["price_change_pct"] >= 0:
                return "ACCUMULATION", 2
            else:
                return "DISTRIBUTION", -2
        return "NEUTRAL", 0

    results = df.apply(classify, axis=1, result_type="expand")
    df["flow_signal"] = results[0]
    df["flow_score"] = results[1]

    return df


# ============================================================
# MAIN RUNNER
# ============================================================
def run():
    df = load_processed_data()
    flow_df = detect_institutional_flow(df)

    output_file = OUTPUT_DIR / "institutional_flow_daily.csv"
    flow_df.to_csv(output_file, index=False)

    print(f"Institutional flow file saved → {output_file}")
    print(flow_df["flow_signal"].value_counts())


if __name__ == "__main__":
    run()
