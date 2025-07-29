from sqlalchemy import update
from anubis.db.schemas.core.user import users
from anubis.db.base import async_session
from firebase_admin import auth

async def mark_user_as_premium(user_id: str):
    # ✅ 1. Update your local DB
    async with async_session() as session:
        await session.execute(
            update(users)
            .where(users.c.firebase_uid == user_id)
            .values(subscription_status="premium")
        )
        await session.commit()

    # ✅ 2. Assign Firebase premium claim
    try:
        auth.set_custom_user_claims(user_id, {"premium": True})
        print(f"✅ Firebase claim set: {user_id} is now premium")
    except Exception as e:
        print(f"❌ Failed to set Firebase claim for {user_id}: {e}")


async def mark_user_as_free(user_id: str, email: str):
    # ✅ 1. Update DB
    async with async_session() as session:
        await session.execute(
            update(users)
            .where(users.c.email == email)
            .values(subscription_status="free")
        )
        await session.commit()

    # ✅ 2. Remove Firebase 'premium' claim
    try:
        auth.set_custom_user_claims(user_id, {})  # wipe all custom claims
        print(f"✅ Firebase claims cleared: {user_id} is now free")
    except Exception as e:
        print(f"❌ Failed to clear Firebase claims for {user_id}: {e}")