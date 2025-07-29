import os

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from anubis.auth.firebase_auth import verify_token
from anubis.db.base import async_session
from anubis.db.schemas.core.user import users

router = APIRouter(prefix="/api")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


@router.post("/auth/persist")
async def persist_user(request: Request, decoded_token=Depends(verify_token)):
    try:
        payload = await request.json()
        print("👀 Payload:", payload)
    except Exception:
        payload = {}

    firebase_uid = decoded_token["uid"]
    email = decoded_token.get("email")
    display_name = decoded_token.get("name")

    print(f"🔥 Got token for UID: {firebase_uid}")

    is_premium = False

    async with async_session() as session:
        # 🧱 Upsert user by Firebase UID
        stmt = insert(users).values(
            firebase_uid=firebase_uid,
            email=email,
            display_name=display_name,
        ).on_conflict_do_update(
            index_elements=["firebase_uid"],
            set_={
                "email": email,
                "display_name": display_name,
            },
        )
        await session.execute(stmt)
        await session.commit()

        # 🔍 Re-fetch user from DB
        result = await session.execute(
            select(users).where(users.c.firebase_uid == firebase_uid)
        )
        existing_user = result.fetchone()

        if not existing_user:
            raise HTTPException(status_code=500, detail="User insert failed")

        # ✅ Check DB subscription status
        db_status = existing_user._mapping.get("subscription_status")
        is_premium = db_status == "premium"

        # 💳 Fallback: Check Stripe subscription only if not premium
        if not is_premium:
            try:
                customers = stripe.Customer.list(email=email).data
                if customers:
                    customer = customers[0]
                    subscriptions = stripe.Subscription.list(
                        customer=customer.id,
                        status="active",
                    ).data
                    if subscriptions:
                        await session.execute(
                            update(users)
                            .where(users.c.firebase_uid == firebase_uid)
                            .values(subscription_status="premium")
                        )
                        await session.commit()
                        is_premium = True
                        print("✅ Stripe subscription found, DB updated to premium.")
            except Exception as e:
                print("⚠️ Stripe lookup failed:", e)

    return {
        "status": "ok",
        "firebase_uid": firebase_uid,
        "is_premium": is_premium,
    }
