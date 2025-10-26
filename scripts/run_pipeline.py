#!/usr/bin/env python
import argparse, json, pathlib
from etl.coingecko import fetch_top_markets
from etl.github import fetch_repo_stats
from scoring.model import score_tokens

BASE = pathlib.Path(__file__).resolve().parents[1]

REPOS = {
    "bitcoin": ("bitcoin", "bitcoin"),
    "ethereum": ("ethereum", "go-ethereum"),
    "solana": ("solana-labs", "solana"),
    "cardano": ("IntersectMBO", "cardano-node"),
    "avalanche-2": ("ava-labs", "avalanchego"),
    "polkadot": ("paritytech", "polkadot-sdk"),
    "chainlink": ("smartcontractkit", "chainlink"),
    "polygon": ("maticnetwork", "heimdall"),
    "litecoin": ("litecoin-project", "litecoin"),
    "monero": ("monero-project", "monero"),
    "stellar": ("stellar", "stellar-core"),
    "cosmos": ("cosmos", "cosmos-sdk"),
    "algorand": ("algorand", "go-algorand"),
    "tezos": ("tezos", "tezos"),
    "zcash": ("zcash", "zcash"),
    "dash": ("dashpay", "dash"),
    "near": ("near", "nearcore"),
    "filecoin": ("filecoin-project", "lotus"),
    "hedera-hashgraph": ("hashgraph", "hedera-services"),
    "fantom": ("Fantom-Foundation", "go-opera"),
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=50, help="Top N coins by market cap")
    args = parser.parse_args()

    raw_path = BASE / "data" / "raw" / "markets.json"
    processed_path = BASE / "data" / "processed" / "scores.json"

    markets = fetch_top_markets(limit=args.top)
    
    for m in markets:
        tid = m.get("id")
        if tid in REPOS:
            owner, repo = REPOS[tid]
            gh = fetch_repo_stats(owner, repo)
            m["gh_commits_30d"] = gh["commits_30d"]
            m["gh_contributors_90d"] = gh["contributors_90d"]
            m["gh_last_push_at"] = gh["last_push_at"]
    
    raw_path.write_text(json.dumps(markets, indent=2))

    scores = score_tokens(markets)
    processed_path.write_text(json.dumps(scores, indent=2))
    print(f"Wrote {processed_path}")

if __name__ == "__main__":
    main()
