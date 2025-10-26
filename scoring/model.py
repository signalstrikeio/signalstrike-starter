from __future__ import annotations
from typing import List, Dict, Any
import math

WEIGHTS = {
    "liquidity_market": 0.25,
    "tokenomics_transparency": 0.20,
    "dev_activity": 0.15,       # placeholder in v1 (fixed neutral)
    "audit_security": 0.15,     # placeholder in v1 (fixed neutral)
    "community_health": 0.15,   # placeholder in v1 (fixed neutral)
    "gov_disclosure": 0.10,     # placeholder in v1 (fixed neutral)
}

def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def _safe_div(a: float, b: float) -> float:
    return a / b if (b and b != 0) else 0.0

def score_tokens(markets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for m in markets:
        volume = float(m.get("total_volume") or 0.0)
        mcap = float(m.get("market_cap") or 0.0)
        circ = float(m.get("circulating_supply") or 0.0)
        total = float(m.get("total_supply") or 0.0)

        # Liquidity & Market: volume/mcap capped at 2.0 (>=200% daily turnover gets full credit)
        vol_to_mcap = _safe_div(volume, mcap)
        liq_norm = _clamp01(vol_to_mcap / 2.0)

        # Tokenomics Transparency: circulating / total (if total missing, use circ/max; if both missing, neutral 0.5)
        if total and total > 0:
            circ_ratio = _clamp01(circ / total)
        else:
            circ_ratio = 0.5

        tokenomics_norm = circ_ratio

        # Developer Activity: Use GitHub stats if available
        commits_30d = float(m.get("gh_commits_30d") or 0.0)
        contrib_90d = float(m.get("gh_contributors_90d") or 0.0)
        commits_norm = max(0.0, min(1.0, commits_30d / 200.0))
        contrib_norm = max(0.0, min(1.0, contrib_90d / 20.0))
        dev_norm = 0.6 * commits_norm + 0.4 * contrib_norm
        
        # Placeholders for v2 (neutral 0.5). Later, wire real data.
        audit_norm = 0.5
        community_norm = 0.5
        gov_norm = 0.5

        pillars = {
            "liquidity_market": round(liq_norm * 100, 2),
            "tokenomics_transparency": round(tokenomics_norm * 100, 2),
            "dev_activity": round(dev_norm * 100, 2),
            "audit_security": round(audit_norm * 100, 2),
            "community_health": round(community_norm * 100, 2),
            "gov_disclosure": round(gov_norm * 100, 2),
        }

        overall = sum(pillars[k] * WEIGHTS[k] for k in WEIGHTS)

        out.append({
            "id": m.get("id"),
            "symbol": m.get("symbol"),
            "name": m.get("name"),
            "price_usd": m.get("current_price"),
            "market_cap_usd": m.get("market_cap"),
            "volume_24h_usd": m.get("total_volume"),
            "circulating_supply": m.get("circulating_supply"),
            "total_supply": m.get("total_supply"),
            "score": round(overall, 2),
            "pillars": pillars,
            "gh_commits_30d": m.get("gh_commits_30d"),
            "gh_contributors_90d": m.get("gh_contributors_90d"),
            "gh_last_push_at": m.get("gh_last_push_at"),
            "explain": {
                "liquidity_market": {
                    "volume_24h_usd": volume,
                    "market_cap_usd": mcap,
                    "vol_to_mcap": vol_to_mcap,
                    "norm_capped_at_2x": round(liq_norm, 4)
                },
                "tokenomics_transparency": {
                    "circulating_supply": circ,
                    "total_supply": total,
                    "circulating_ratio": round(tokenomics_norm, 4)
                },
                "dev_activity": {
                    "gh_commits_30d": m.get("gh_commits_30d"),
                    "gh_contributors_90d": m.get("gh_contributors_90d"),
                    "has_github_data": m.get("gh_commits_30d") is not None,
                    "norm": round(dev_norm, 4)
                },
                "notes": "Audit, community, governance are neutral in v2; wire real sources later."
            }
        })
    # Sort by score desc
    out.sort(key=lambda r: r["score"], reverse=True)
    return out
