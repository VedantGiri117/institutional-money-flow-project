import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw" / "bhavcopy"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD LATEST RAW FILE
# ============================================================
def load_latest_bhavcopy() -> pd.DataFrame:
    files = sorted(RAW_DIR.glob("bhavcopy_*.csv"))
    if not files:
        raise FileNotFoundError("No raw bhavcopy files found")
    return pd.read_csv(files[-1])


# ============================================================
# CLEAN DATA
# ============================================================
def clean_bhavcopy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Ensure numeric columns
    numeric_cols = ["open", "high", "low", "close", "volume", "price_change_pct"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with missing critical values
    df.dropna(subset=["open", "high", "low", "close", "volume"], inplace=True)

    # Sort by volume (descending)
    df.sort_values(by="volume", ascending=False, inplace=True)

    df.reset_index(drop=True, inplace=True)
    return df


# ============================================================
# MAIN RUNNER
# ============================================================
def run():
    df = load_latest_bhavcopy()
    clean_df = clean_bhavcopy(df)

    output_file = PROCESSED_DIR / "bhavcopy_processed.csv"
    clean_df.to_csv(output_file, index=False)

    print(f"Processed bhavcopy saved → {output_file}")
    print("Rows:", len(clean_df))
    print("Columns:", list(clean_df.columns))


if __name__ == "__main__":
    run()
