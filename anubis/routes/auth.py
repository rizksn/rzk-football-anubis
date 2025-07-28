import os
import stripe
from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from anubis.auth.firebase_auth import verify_token
from anubis.db.schemas.core.user import users
from anubis.db.base import async_session  

router = APIRouter(prefix="/api")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/auth/persist")
async def persist_user(request: Request, decoded_token=Depends(verify_token)):
    try:
        payload = await request.json()
        print("👀 Payload:", payload)
    except Exception:
        payload = {}

    print("🔥 Got token for UID:", decoded_token["uid"])
    firebase_uid = decoded_token["uid"]
    email = decoded_token.get("email")
    display_name = decoded_token.get("name")

    is_premium = False

    async with async_session() as session:
        # Fetch existing user
        result = await session.execute(
            select(users).where(users.c.firebase_uid == firebase_uid)
        )
        existing_user = result.fetchone()

        # Insert user if not found
        if not existing_user:
            await session.execute(users.insert().values(
                firebase_uid=firebase_uid,
                email=email,
                display_name=display_name,
            ))
            await session.commit()
            print("👤 Created new user.")

            # Re-fetch after insert
            result = await session.execute(
                select(users).where(users.c.firebase_uid == firebase_uid)
            )
            existing_user = result.fetchone()

        # ✅ Check subscription_status in DB
        if existing_user:
            db_subscription_status = existing_user._mapping.get("subscription_status")
            is_premium = db_subscription_status == "premium"

        # 🟡 Only call Stripe if not premium
        if not is_premium:
            try:
                customers = stripe.Customer.list(email=email).data
                if customers:
                    stripe_customer = customers[0]
                    subscriptions = stripe.Subscription.list(
                        customer=stripe_customer.id,
                        status="active"
                    ).data
                    if subscriptions:
                        await session.execute(
                            users.update()
                            .where(users.c.firebase_uid == firebase_uid)
                            .values(subscription_status="premium")
                        )
                        await session.commit()
                        is_premium = True
                        print(f"✅ Stripe subscription found, DB updated to premium.")
            except Exception as e:
                print("⚠️ Stripe lookup failed:", e)

    return {
        "status": "ok",
        "firebase_uid": firebase_uid,
        "is_premium": is_premium
    }
