import os
import stripe
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from anubis.auth.firebase_auth import verify_token

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/api")

# This should be your actual Stripe Price ID from your $0.99/mo product
PREMIUM_PRICE_ID = os.getenv("STRIPE_PREMIUM_PRICE_ID")

@router.post("/stripe/checkout")
async def create_checkout_session(decoded_token=Depends(verify_token)):
    """
    Create a Stripe Checkout session for a monthly subscription.
    Firebase auth token is verified via Depends.
    """
    try:
        user_id = decoded_token["uid"]
        email = decoded_token.get("email")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",  # 👈 MONTHLY SUBSCRIPTION
            customer_email=email,
            line_items=[
                {
                    "price": PREMIUM_PRICE_ID,  # 👈 your Stripe Price ID
                    "quantity": 1,
                }
            ],
            metadata={
                "user_id": user_id,
                "email": email,
            },
            success_url=f"{frontend_url}/success",
            cancel_url=f"{frontend_url}/cancel",
        )

        return {"url": session.url}

    except Exception as e:
        print("❌ Stripe session creation error:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
