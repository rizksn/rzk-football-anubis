from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from anubis.db.base import async_session

router = APIRouter(prefix="/api")

VALID_FORMATS = {
    "dynasty_1qb_1_ppr_sleeper",
    "redraft_1qb_0_5_ppr_consensus",
    "rookie_1qb_1_ppr_sleeper",
    # Add all valid format table names here
}

@router.get("/players")
async def get_players(format: str = Query("dynasty_1qb_1_ppr_sleeper")):
    if format not in VALID_FORMATS:
        raise HTTPException(status_code=400, detail="Invalid format")

    async with async_session() as session:  
        try:
            query = text(f'SELECT * FROM market."{format}"')
            result = await session.execute(query)
            players = [dict(row._mapping) for row in result.fetchall()]
            return {"data": players}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"DB error: {e}")