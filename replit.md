# SignalStrike - Crypto Credibility Tracker

## Overview
SignalStrike is a data-first crypto credibility tracker that pulls market data from CoinGecko, computes transparent 0-100 scores for tokens, and serves them via a FastAPI endpoint.

**Current State**: Configured and running on Replit with sample data for top 50 cryptocurrencies.

## Recent Changes
- **2025-10-26**: GitHub Integration Added
  - Added GitHub repository stats tracking (commits, contributors, last push)
  - Enhanced developer activity scoring using real GitHub data
  - Added 20 cryptocurrency GitHub repository mappings
  - Updated scoring model to calculate dev_activity from GitHub metrics
  - Bitcoin now shows 100% dev activity (176 commits, 100 contributors)
  
- **2025-10-26**: Initial Replit setup
  - Installed Python dependencies (FastAPI, uvicorn, httpx, pydantic, pandas)
  - Created data directories and ran initial ETL pipeline
  - Configured API workflow to run on port 5000
  - Generated scores for top cryptocurrencies

## Project Architecture

### Structure
```
.
├── api/
│   └── main.py          # FastAPI application with token endpoints
├── etl/
│   ├── coingecko.py     # CoinGecko data fetching
│   └── github.py        # GitHub repository stats fetching
├── scoring/
│   └── model.py         # Token scoring algorithm (with GitHub integration)
├── scripts/
│   └── run_pipeline.py  # ETL pipeline runner (includes GitHub enrichment)
├── data/
│   ├── raw/            # Raw CoinGecko + GitHub data
│   └── processed/      # Computed scores with GitHub metrics
└── requirements.txt
```

### Supported Cryptocurrencies with GitHub Data
Bitcoin, Ethereum, Solana, Cardano, Avalanche, Polkadot, Chainlink, Polygon, Litecoin, Monero, Stellar, Cosmos, Algorand, Tezos, Zcash, Dash, NEAR, Filecoin, Hedera, Fantom

### Technology Stack
- **Backend**: FastAPI + Uvicorn
- **Data**: CoinGecko API (no API key required)
- **Processing**: pandas, httpx
- **Python**: 3.11

### Scoring Methodology
The SignalStrike score (0-100) uses weighted pillars:
- **Liquidity/Market (25%)**: Volume-to-market-cap ratio (capped at 200% daily turnover)
- **Tokenomics Transparency (20%)**: Circulating vs total supply ratio
- **Dev Activity (15%)**: **NOW LIVE** - GitHub commits (60%) + contributors (40%)
  - Uses real data from GitHub API for 20 major cryptocurrencies
  - Scores: >100 commits/month = 100%, >50 contributors = 100%
- **Audit/Security (15%)**: Placeholder (neutral 50) - coming in v2
- **Community Health (15%)**: Placeholder (neutral 50) - coming in v2
- **Gov/Disclosure (10%)**: Placeholder (neutral 50) - coming in v2

### API Endpoints
- `GET /v1/tokens` - List all tokens with scores (supports limit/offset)
- `GET /v1/tokens/{id}` - Get detailed token info by ID
- `GET /docs` - Interactive API documentation

### Running Locally
1. **Update Data**: `PYTHONPATH=/home/runner/workspace python scripts/run_pipeline.py --top 100`
2. **Start API**: Workflow automatically runs on port 5000

## User Preferences
None documented yet.

## Future Roadmap
- Add GitHub developer activity metrics
- Add audit/security signals
- Persist history in database (SQLite/Postgres)
- Build frontend dashboard (Next.js)
