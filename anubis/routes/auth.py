from fastapi import APIRouter, Depends
from anubis.auth.firebase_auth import verify_token
from anubis.db.schemas.core.user import users
from anubis.db import database

router = APIRouter()

@router.post("/auth/persist")
async def persist_user(decoded_token=Depends(verify_token)):
    firebase_uid = decoded_token["uid"]
    email = decoded_token.get("email")
    display_name = decoded_token.get("name")

    # Check if user already exists
    existing_user = await database.fetch_one(
        users.select().where(users.c.firebase_uid == firebase_uid)
    )

    if not existing_user:
        await database.execute(users.insert().values(
            firebase_uid=firebase_uid,
            email=email,
            display_name=display_name
        ))

    return {"status": "ok", "firebase_uid": firebase_uid}