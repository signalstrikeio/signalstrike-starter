# SignalStrike (Starter)

A minimal, **data-first** crypto credibility tracker.

This starter lets you:
1) Pull market data for the top N coins from CoinGecko
2) Compute a transparent 0–100 **SignalStrike Score** for each token
3) Serve the latest scores via a simple FastAPI endpoint

> Built to be run on your local machine, GitHub Codespaces, or Replit.

---

## Quick Start

### 0) Prereqs
- Python 3.10+
- `pip install -r requirements.txt`

### 1) Run the pipeline (ETL -> Score -> JSON)
```bash
python scripts/run_pipeline.py --top 100
```

This will create:
- `data/raw/markets.json` (raw CoinGecko snapshot)
- `data/processed/scores.json` (scores + pillar breakdowns)

### 2) Run the API
```bash
uvicorn api.main:app --reload --port 8000
```
Open http://127.0.0.1:8000 to see docs. Endpoints:
- `GET /v1/tokens` (list with scores)
- `GET /v1/tokens/{id}` (detail)

---

## Notes
- No API keys required for v1 (CoinGecko public endpoints).
- Scores are **illustrative**; tweak weights/normalization in `scoring/model.py`.
- Methodology is transparent by design—see `explain` fields in responses.

## Roadmap
- Add GitHub developer activity metric
- Add audit/security signals
- Persist history in SQLite/Postgres
- Frontend (Next.js) table + token detail
