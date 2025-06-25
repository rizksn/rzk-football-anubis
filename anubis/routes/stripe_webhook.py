import stripe
import os
from fastapi import APIRouter, Request, HTTPException, status
from anubis.services.users import mark_user_as_premium

router = APIRouter(prefix="/api/stripe")

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Stripe webhook secret not configured.")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid Stripe signature.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

    # 🔔 Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print("✅ Checkout complete:", session["id"])

        # 🔍 Log metadata in development for debugging
        if os.getenv("ENV") == "development":
            print("📦 Session metadata:", session.get("metadata", {}))

        user_id = session.get("metadata", {}).get("user_id")
        if user_id:
            await mark_user_as_premium(user_id)
            print(f"🎉 Upgraded user {user_id} to premium")
        else:
            print("⚠️ No user_id found in session metadata")
