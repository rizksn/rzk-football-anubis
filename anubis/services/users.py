from sqlalchemy import update
from anubis.db.schemas.core.user import users
from anubis.db.base import async_session
from firebase_admin import auth

async def mark_user_as_premium(user_id: str):
    async with async_session() as session:
        # Update local DB subscription status
        await session.execute(
            update(users)
            .where(users.c.firebase_uid == user_id)
            .values(subscription_status="premium")
        )
        await session.commit()

    try:
        # Fetch current Firebase claims and add premium
        user = auth.get_user(user_id)
        existing_claims = user.custom_claims or {}
        existing_claims["premium"] = True
        auth.set_custom_user_claims(user_id, existing_claims)
        print(f"✅ Firebase claim set: {user_id} is now premium")
    except Exception as e:
        print(f"❌ Failed to set Firebase claim for {user_id}: {e}")


async def mark_user_as_free(user_id: str, email: str):
    async with async_session() as session:
        # Update local DB subscription status to free
        await session.execute(
            update(users)
            .where(users.c.email == email)
            .values(subscription_status="free")
        )
        await session.commit()

    try:
        # Fetch current Firebase claims and remove premium key only
        user = auth.get_user(user_id)
        existing_claims = user.custom_claims or {}
        existing_claims.pop("premium", None)
        auth.set_custom_user_claims(user_id, existing_claims)
        print(f"✅ Firebase claims updated: {user_id} is now free")
    except Exception as e:
        print(f"❌ Failed to update Firebase claims for {user_id}: {e}")
