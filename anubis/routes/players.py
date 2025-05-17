import os
import json
from fastapi import APIRouter, HTTPException
from pathlib import Path

router = APIRouter()

DATA_PATH = Path(__file__).resolve().parent.parent / 'data' / 'adp-consensus-ppr.json'

@router.get("/players")
def get_adp_players():
    try:
        with open(DATA_PATH, 'r') as f:
            data = json.load(f)
            return data.get("data", [])
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="ADP data not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading ADP data: {e}")