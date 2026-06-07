import requests
import pandas as pd
from datetime import datetime, timedelta, time
from pathlib import Path
import pytz


# ============================================================
# PATH SETUP
# ============================================================
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw" / "bhavcopy"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# NSE SESSION (ANTI-BOT SAFE)
# ============================================================
def get_nse_session() -> requests.Session:
    """
    Creates a browser-like session required by NSE APIs
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com",
        "Connection": "keep-alive"
    })

    # First hit homepage to get cookies
    session.get("https://www.nseindia.com", timeout=10)
    return session


# ============================================================
# TIME-AWARE TRADE DATE (IST)
# ============================================================
def get_trade_date():
    """
    Time rules (IST):
    - 12:00 AM – 9:00 AM  → previous trading day
    - 9:01 AM – 11:59 PM → today
    """
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    if now.time() <= time(9, 0):
        return (now - timedelta(days=1)).date()
    return now.date()


# ============================================================
# FETCH NSE INDEX DATA (JSON)
# ============================================================
def fetch_index_data(session: requests.Session, index_name: str) -> pd.DataFrame:
    """
    Fetches index constituents data from NSE JSON API
    """
    url = "https://www.nseindia.com/api/equity-stockIndices"
    params = {"index": index_name}

    response = session.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()
    return pd.DataFrame(data["data"])


# ============================================================
# MAIN RUNNER
# ============================================================
def run():
    session = get_nse_session()
    trade_date = get_trade_date()

    print(f"Fetching NSE data for trade date: {trade_date}")

    # Fetch NIFTY 50 and NIFTY 100
    df_nifty_50 = fetch_index_data(session, "NIFTY 50")
    df_nifty_100 = fetch_index_data(session, "NIFTY 100")

    # Combine and remove duplicates
    df = pd.concat([df_nifty_50, df_nifty_100], ignore_index=True)
    df.drop_duplicates(subset="symbol", inplace=True)

    # Keep only required columns
    df = df[[
        "symbol",
        "open",
        "dayHigh",
        "dayLow",
        "lastPrice",
        "totalTradedVolume",
        "pChange"
    ]]

    # Rename columns to bhavcopy-like format
    df.rename(columns={
        "dayHigh": "high",
        "dayLow": "low",
        "lastPrice": "close",
        "totalTradedVolume": "volume",
        "pChange": "price_change_pct"
    }, inplace=True)

    # Save output
    output_file = RAW_DATA_DIR / f"bhavcopy_{trade_date}.csv"
    df.to_csv(output_file, index=False)

    print(f"Saved raw NSE data → {output_file}")
    print(f"Total stocks saved: {len(df)}")
    print("Columns:", list(df.columns))


if __name__ == "__main__":
    run()
