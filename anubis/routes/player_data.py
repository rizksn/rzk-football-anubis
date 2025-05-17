# backend/anubis/routes/player_data.py

from fastapi import APIRouter
from typing import List, Dict
from anubis.scrapers.nfl_stats import fetch_nfl_stats

router = APIRouter()

@router.get("/player-data/{stat_type}/{year}")
async def get_player_data(stat_type: str = "rushing", year: int = 2024) -> List[Dict]:
    return await fetch_nfl_stats(stat_type=stat_type, year=year)