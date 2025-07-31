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

    if not payload.player_ids:
        raise HTTPException(status_code=400, detail="No player_ids provided")

    if len(payload.player_ids) != len(set(payload.player_ids)):
        raise HTTPException(status_code=400, detail="Duplicate player_ids in rankings")

    # Delete existing row for this user/format
    await db.execute(
        delete(adp_format_rankings).where(
            adp_format_rankings.c.user_id == user_id,
            adp_format_rankings.c.adp_format_key == payload.adp_format_key
        )
    )

    # Insert new row with JSONB rankings list
    await db.execute(
        insert(adp_format_rankings).values(
            user_id=user_id,
            adp_format_key=payload.adp_format_key,
            rankings=payload.player_ids  # 👈 just save the full list
        )
    )

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
    )

    result = await db.execute(stmt)
    rows = result.mappings().all()

    return {
        "rankings": rows[0]["rankings"] if rows else []
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
