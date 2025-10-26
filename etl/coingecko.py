import httpx

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

def fetch_top_markets(limit: int = 50, vs_currency: str = "usd"):
    """
    Returns a list of dicts with fields:
    id, symbol, name, current_price, market_cap, total_volume, circulating_supply, total_supply
    """
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": min(limit, 250),
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "24h",
    }
    results = []
    remaining = limit
    page = 1
    while remaining > 0:
        params["page"] = page
        params["per_page"] = min(remaining, 250)
        with httpx.Client(timeout=30) as client:
            r = client.get(COINGECKO_URL, params=params)
            r.raise_for_status()
            chunk = r.json()
            if not chunk:
                break
            results.extend(chunk)
        remaining -= len(chunk)
        page += 1
    # Keep only needed fields
    keep = ("id","symbol","name","current_price","market_cap","total_volume",
            "circulating_supply","total_supply","max_supply")
    trimmed = [{k: item.get(k) for k in keep} for item in results]
    return trimmed
