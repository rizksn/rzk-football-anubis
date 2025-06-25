from sqlalchemy import update
from anubis.db.schemas.core.user import users
from anubis.db.base import async_session

async def mark_user_as_premium(firebase_uid: str):
    async with async_session() as session:
        await session.execute(
            update(users)
            .where(users.c.firebase_uid == firebase_uid) 
            .values(subscription_status="premium")
        )
        await session.commit()
