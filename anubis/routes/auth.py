import os
import stripe
from fastapi import APIRouter, Depends
from sqlalchemy import select
from anubis.auth.firebase_auth import verify_token
from anubis.db.schemas.core.user import users
from anubis.db.base import async_session  

router = APIRouter(prefix="/api")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/auth/persist")
async def persist_user(decoded_token=Depends(verify_token)):
    print("🔥 Got token for UID:", decoded_token["uid"])
    firebase_uid = decoded_token["uid"]
    email = decoded_token.get("email")
    display_name = decoded_token.get("name")

    async with async_session() as session:
        result = await session.execute(
            select(users).where(users.c.firebase_uid == firebase_uid)
        )
        existing_user = result.fetchone()

        if not existing_user:
            await session.execute(users.insert().values(
                firebase_uid=firebase_uid,
                email=email,
                display_name=display_name
            ))
            await session.commit()

    # 🔍 Check Stripe for active subscription
    stripe_customer = None
    has_paid = False

    try:
        customers = stripe.Customer.list(email=email).data
        if customers:
            stripe_customer = customers[0]
            subscriptions = stripe.Subscription.list(
                customer=stripe_customer.id,
                status="active"
            ).data
            if subscriptions:
                has_paid = True
    except Exception as e:
        print("⚠️ Stripe lookup failed:", e)

    return {
        "status": "ok",
        "firebase_uid": firebase_uid,
        "stripe_active": has_paid
    }
