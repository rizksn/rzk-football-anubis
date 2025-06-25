from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import stripe
import os

router = APIRouter(prefix="/api")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    try:
        body = await request.json()
        user_id = body.get("user_id")  

        YOUR_DOMAIN = os.getenv("FRONTEND_URL", "http://localhost:3000")

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            metadata={   
                "user_id": user_id
            },
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Redraft Unlock – $0.99',
                    },
                    'unit_amount': 99,
                },
                'quantity': 1,
            }],
            success_url=f"{YOUR_DOMAIN}/success",
            cancel_url=f"{YOUR_DOMAIN}/cancel",
        )

        return {"url": session.url}

    except Exception as e:
        print("❌ Stripe session creation error:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})

