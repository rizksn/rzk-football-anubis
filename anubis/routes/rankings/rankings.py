from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from anubis.db.session import get_async_session
from anubis.db.schemas.core.adp_format_rankings import adp_format_rankings
from anubis.auth.firebase_auth import verify_token
from anubis.routes.schemas.ranking import FormatRankingPayload

router = APIRouter()

@router.post("/save")
async def save_rankings(
    payload: FormatRankingPayload,
    decoded_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_async_session),
):
    if not decoded_user.get("premium", False):
        raise HTTPException(status_code=403, detail="Premium access required")

    user_id = decoded_user["uid"]

    # Delete any existing rankings for this user/format
    await db.execute(
        delete(adp_format_rankings).where(
            adp_format_rankings.c.user_id == user_id,
            adp_format_rankings.c.adp_format_key == payload.adp_format_key
        )
    )

    # Insert updated rankings
    values = [
        {
            "user_id": user_id,
            "adp_format_key": payload.adp_format_key,
            "player_id": player_id,
            "rank": rank
        }
        for rank, player_id in enumerate(payload.player_ids, start=1)
    ]

    await db.execute(insert(adp_format_rankings), values)
    await db.commit()
    return {"success": True, "message": "Rankings saved"}


@router.get("/load")
async def load_rankings(
    format_key: str,
    decoded_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_async_session),
):
    if not decoded_user.get("premium", False):
        raise HTTPException(status_code=403, detail="Premium access required")

    user_id = decoded_user["uid"]

    stmt = select(adp_format_rankings).where(
        adp_format_rankings.c.user_id == user_id,
        adp_format_rankings.c.adp_format_key == format_key
    ).order_by(adp_format_rankings.c.rank)

    result = await db.execute(stmt)
    rows = result.mappings().all()

    return {
        "rankings": [row["player_id"] for row in rows]
    }


@router.delete("/{format_key}")
async def delete_rankings(
    format_key: str,
    decoded_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_async_session),
):
    user_id = decoded_user["uid"]

    await db.execute(
        delete(adp_format_rankings).where(
            adp_format_rankings.c.user_id == user_id,
            adp_format_rankings.c.adp_format_key == format_key
        )
    )
    await db.commit()
    return {"success": True, "message": "Rankings deleted"}
