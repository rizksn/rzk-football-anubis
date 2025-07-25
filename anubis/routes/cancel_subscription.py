from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import update
import os
import stripe

from anubis.auth.firebase_auth import verify_token
from anubis.db.base import async_session
from anubis.db.schemas.core.user import users

router = APIRouter(prefix="/api/stripe")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/cancel")
async def cancel_subscription(decoded_token=Depends(verify_token)):
    email = decoded_token.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Missing user email")

    try:
        customers = stripe.Customer.list(email=email).data
        if not customers:
            raise HTTPException(status_code=404, detail="Stripe customer not found")

        customer = customers[0]
        subscriptions = stripe.Subscription.list(
            customer=customer.id, status="active"
        ).data

        if not subscriptions:
            return JSONResponse(status_code=200, content={"message": "No active subscription found"})

        for sub in subscriptions:
            stripe.Subscription.delete(sub.id)

        # Downgrade user in DB
        async with async_session() as session:
            await session.execute(
                update(users)
                .where(users.c.email == email)
                .values(subscription_status='free')
            )
            await session.commit()

        return {"message": "Subscription canceled successfully"}

    except Exception as e:
        print("❌ Cancel subscription error:", str(e))
        raise HTTPException(status_code=500, detail="Failed to cancel subscription")
