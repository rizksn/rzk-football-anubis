from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from anubis.db.base import async_session
from anubis.utils.adp_utils import get_valid_adp_keys

router = APIRouter(prefix="/api")

VALID_FORMATS = get_valid_adp_keys()

@router.get("/players")
async def get_players(format: str = Query("dynasty_1qb_1_ppr_sleeper")):
    if format not in VALID_FORMATS:
        raise HTTPException(status_code=400, detail="Invalid format")

    async with async_session() as session:
        try:
            query = text(f'SELECT * FROM market."{format}"')
            result = await session.execute(query)
            adp_players = [dict(row._mapping) for row in result.fetchall()]

            from anubis.draft_engine.scoring.adp_scoring import score_players
            scored_players = score_players(adp_players)

            return {
                "adp": adp_players,        # used for display in ADP tab
                "scored": scored_players   # used for simulation
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"DB error: {e}")
