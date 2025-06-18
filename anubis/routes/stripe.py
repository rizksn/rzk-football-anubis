from fastapi import APIRouter, HTTPException
import stripe
import os
from starlette.requests import Request

router = APIRouter(prefix="/api")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    try:
        YOUR_DOMAIN = "http://localhost:3000"  # Change to your deployed frontend later

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Redraft Unlock – $0.99',
                    },
                    'unit_amount': 99,  # $0.99 in cents
                },
                'quantity': 1,
            }],
            success_url=YOUR_DOMAIN + "/success",
            cancel_url=YOUR_DOMAIN + "/cancel",
        )
        return {"id": checkout_session.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
