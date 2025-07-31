from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update

from anubis.db.session import get_async_session
from anubis.db.schemas.core.keeper_sets import keeper_sets
from anubis.auth.firebase_auth import verify_token
from anubis.routes.schemas.keeper import KeeperSetPayload


router = APIRouter()

@router.post("/save")
async def save_keepers(
    payload: KeeperSetPayload,
    decoded_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_async_session),
):
    if not decoded_user.get("premium", False):
        raise HTTPException(status_code=403, detail="Premium access required")

    user_id = decoded_user["uid"]

    # ✅ Check if keeper set already exists
    stmt = select(keeper_sets).where(
        keeper_sets.c.user_id == user_id,
        keeper_sets.c.name == payload.name
    )
    result = await db.execute(stmt)
    existing_keeper = result.fetchone()

    values = {
        "format_key": payload.format_key,
        "num_teams": payload.num_teams,
        "draft_plan": [pick.dict() for pick in payload.draft_plan],
    }

    if existing_keeper:
        stmt = update(keeper_sets).where(
            keeper_sets.c.user_id == user_id,
            keeper_sets.c.name == payload.name
        ).values(**values)
    else:
        stmt = insert(keeper_sets).values(
            user_id=user_id,
            name=payload.name,
            **values
        )

    await db.execute(stmt)
    await db.commit()
    return {"success": True, "message": "Keepers saved"}


@router.get("/load")
async def load_keepers(
    name: str = None,
    format_key: str = None,
    decoded_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_async_session),
):
    if not decoded_user.get("premium", False):
        raise HTTPException(status_code=403, detail="Premium access required")

    user_id = decoded_user["uid"]

    stmt = select(keeper_sets).where(keeper_sets.c.user_id == user_id)

    if name:
        stmt = stmt.where(keeper_sets.c.name == name)

    if format_key:
        stmt = stmt.where(keeper_sets.c.format_key == format_key)

    result = await db.execute(stmt)
    rows = result.mappings().all()

    serialized = [
        {
            "id": row["id"],
            "user_id": row["user_id"],
            "name": row["name"],
            "format_key": row["format_key"],
            "num_teams": row["num_teams"],
            "draft_plan": row["draft_plan"],
        }
        for row in rows
    ]

    return {"keeper_sets": serialized}


@router.get("/{keeper_id}")
async def get_keeper_set_by_id(
    keeper_id: str,
    decoded_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_async_session),
):
    if not decoded_user.get("premium", False):
        raise HTTPException(status_code=403, detail="Premium access required")

    stmt = select(keeper_sets).where(keeper_sets.c.id == keeper_id)
    result = await db.execute(stmt)
    row = result.mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Keeper set not found")

    if row["user_id"] != decoded_user["uid"]:
        raise HTTPException(status_code=403, detail="Not authorized to access this keeper set")

    return {
        "id": row["id"],
        "name": row["name"],
        "format_key": row["format_key"],
        "num_teams": row["num_teams"],
        "draft_plan": row["draft_plan"],
    }


@router.delete("/{keeper_id}")
async def delete_keeper_set(
    keeper_id: int,
    decoded_user: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_async_session),
):
    stmt = select(keeper_sets).where(keeper_sets.c.id == keeper_id)
    result = await db.execute(stmt)
    row = result.mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Keeper set not found")

    if row["user_id"] != decoded_user["uid"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this keeper set")

    await db.execute(keeper_sets.delete().where(keeper_sets.c.id == keeper_id))
    await db.commit()
    return {"success": True, "message": "Keeper set deleted"}
