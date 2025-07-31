from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict

from anubis.db.session import get_async_session
from anubis.db.schemas.nfl.nfl_player_qb_2024 import nfl_player_qb_2024
from anubis.db.schemas.nfl.nfl_player_rb_2024 import nfl_player_rb_2024
from anubis.db.schemas.nfl.nfl_player_wr_2024 import nfl_player_wr_2024
from anubis.db.schemas.nfl.nfl_player_te_2024 import nfl_player_te_2024
from anubis.db.schemas.nfl.nfl_player_kicking_2024 import nfl_player_kicking_2024

router = APIRouter(prefix="/api")

# Map stat_type to correct table
STAT_TABLE_MAP = {
    "qb": nfl_player_qb_2024,
    "rb": nfl_player_rb_2024,
    "wr": nfl_player_wr_2024,
    "te": nfl_player_te_2024,
    "k": nfl_player_kicking_2024,
}

@router.get("/player-data/{stat_type}/{year}")
async def get_player_data(stat_type: str = "qb", year: int = 2024, player_id: str = None) -> List[Dict]:
    if year != 2024:
        raise HTTPException(status_code=400, detail="Only 2024 data supported for now.")

    table = STAT_TABLE_MAP.get(stat_type.lower())
    if table is None:
        raise HTTPException(status_code=400, detail=f"Unsupported stat_type: {stat_type}")

    async with get_async_session() as session:
        query = select(table)
        if player_id:
            query = query.where(table.c.player_id == player_id)

        result = await session.execute(query)
        rows = result.mappings().all()

    return [dict(row) for row in rows]
