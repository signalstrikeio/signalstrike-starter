#!/usr/bin/env python
import argparse, json, pathlib
from etl.coingecko import fetch_top_markets
from scoring.model import score_tokens

BASE = pathlib.Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=50, help="Top N coins by market cap")
    args = parser.parse_args()

    raw_path = BASE / "data" / "raw" / "markets.json"
    processed_path = BASE / "data" / "processed" / "scores.json"

    markets = fetch_top_markets(limit=args.top)
    raw_path.write_text(json.dumps(markets, indent=2))

    scores = score_tokens(markets)
    processed_path.write_text(json.dumps(scores, indent=2))
    print(f"Wrote {processed_path}")

if __name__ == "__main__":
    main()
