import json
import pandas as pd
from pathlib import Path
from google import genai


# ============================================================
# PATHS
# ============================================================
BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = BASE_DIR / "configs"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = PROCESSED_DIR
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD CONFIG & DATA
# ============================================================
def load_ai_config():
    with open(CONFIG_DIR / "ai_config.json", "r") as f:
        return json.load(f)


def load_top10():
    file_path = PROCESSED_DIR / "top10_institutional_picks.csv"
    if not file_path.exists():
        raise FileNotFoundError("Top 10 picks file not found")
    return pd.read_csv(file_path)


# ============================================================
# PROMPT BUILDER
# ============================================================
def build_prompt(df: pd.DataFrame) -> str:
    lines = []
    for _, row in df.iterrows():
        lines.append(
            f"- {row['symbol']}: signal={row['flow_signal']}, "
            f"score={row['flow_score']}, volume={int(row['volume'])}"
        )

    stocks_block = "\n".join(lines)

    prompt = f"""
You are a professional Indian equity market analyst.

Below are the Top 10 stocks showing institutional money flow today
based on volume and price behavior.

Stocks:
{stocks_block}

Tasks:
1. Explain in 7–10 bullet points why institutions are active today.
2. Mention common patterns across these stocks.
3. Suggest a suitable investment horizon (intraday / swing / positional).
4. Add 3 concise risk warnings.
5. Keep tone neutral and professional (no hype).
"""
    return prompt.strip()


# ============================================================
# GEMINI CALL (NEW SDK)
# ============================================================
def generate_summary(prompt: str, config: dict) -> str:
    client = genai.Client(api_key=config["api_key"])

    response = client.models.generate_content(
        model=config.get("model", "models/gemini-2.5-flash"),
        contents=[
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    )

    return response.text


# ============================================================
# MAIN RUNNER
# ============================================================
def run():
    config = load_ai_config()
    df = load_top10()
    prompt = build_prompt(df)

    print("Generating AI summary via Gemini (new SDK)...")
    summary = generate_summary(prompt, config)

    output_file = OUTPUT_DIR / "ai_investment_summary.txt"
    with open(output_file, "w") as f:
        f.write(summary)

    print(f"AI summary saved → {output_file}")
    print("\n--- AI SUMMARY PREVIEW ---\n")
    print(summary)


if __name__ == "__main__":
    run()
