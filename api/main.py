from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
import json, pathlib

app = FastAPI(title="SignalStrike API", version="0.1.0")

BASE = pathlib.Path(__file__).resolve().parents[1]
SCORES_PATH = BASE / "data" / "processed" / "scores.json"

def _load_scores() -> List[Dict[str, Any]]:
    if not SCORES_PATH.exists():
        return []
    return json.loads(SCORES_PATH.read_text())

@app.get("/v1/tokens", summary="List tokens with latest scores")
def list_tokens(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    data = _load_scores()
    return data[offset: offset + limit]

@app.get("/v1/tokens/{token_id}", summary="Get one token by id")
def get_token(token_id: str) -> Dict[str, Any]:
    data = _load_scores()
    for item in data:
        if item.get("id") == token_id:
            return item
    raise HTTPException(status_code=404, detail="Token not found")
