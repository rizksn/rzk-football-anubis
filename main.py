# ─── 📦 Standard Library ─────────────────────────────
import os

# ─── 🔧 Third-party ──────────────────────────────────
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ─── 📡 Environment ──────────────────────────────────
ENV = os.getenv("ENV", "production").lower()
IS_DEV = ENV == "development"

print(f"🚀 Starting FastAPI in {ENV.upper()} mode")

# ─── 🔐 CORS Configuration ───────────────────────────
allow_origins = [
    "https://rzkfootball.com",
    "https://rzk-anubis.onrender.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

print(f"🔐 CORS allowed origins: {allow_origins}")

# ─── ⚙️ App Setup ─────────────────────────────────────
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── 🧱 Optional: Block localhost in production routes ─────────
def block_local_requests_in_prod(request: Request):
    if ENV == "production" and request.client.host.startswith("127."):
        raise HTTPException(status_code=403, detail="Local access not allowed in production")

# ─── 📁 Routers ──────────────────────────────────────
from anubis.routes import auth as auth_routes
from anubis.routes.adp_data import router as players_router
from anubis.routes.simulate import router as simulate_router
from anubis.routes.player_data import router as player_data_router
from anubis.routes.checkout import router as stripe_router
from anubis.routes import stripe_webhook 
from anubis.routes.cancel_subscription import router as cancel_router

ROUTERS = [
    players_router,
    simulate_router,
    player_data_router,
    stripe_router,
    cancel_router, 
    auth_routes.router,
    stripe_webhook.router, 
]

for router in ROUTERS:
    app.include_router(router)

# ─── 🩺 Health Check ─────────────────────────────────
@app.get("/")
async def read_root(request: Request):
    # Optional production safeguard
    block_local_requests_in_prod(request)
    return {"message": "Backend is up and running!"}