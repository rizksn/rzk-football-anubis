from fastapi import APIRouter
from typing import List, Dict
import json
from anubis.scrapers.nfl.fetch_player_season_stats_nfl import fetch_player_season_stats

router = APIRouter()

@router.get("/player-data/{stat_type}/{year}")
async def get_player_data(stat_type: str = "rushing", year: int = 2024) -> List[Dict]:
    await fetch_player_season_stats(stat_type=stat_type, year=year)
    with open(f"anubis/data/raw/nfl/nfl_player_{stat_type}_{year}.raw.json", "r") as f:
        return json.load(f)