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
from anubis.routes.auth import auth as auth_routes
from anubis.routes.adp.adp_data import router as players_router
from anubis.routes.simulate import router as simulate_router
from anubis.routes.draft.player_data import router as player_data_router
from anubis.routes.checkout.checkout import router as stripe_router
from anubis.routes.auth import stripe_webhook 
from anubis.routes.auth.cancel_subscription import router as cancel_router
from anubis.routes.keepers import router as keepers_router
from anubis.routes.rankings import router as rankings_router

# Routers with no prefix embedded
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

# ✅ Explicitly add keeper routes with a prefix
app.include_router(keepers_router, prefix="/api/keepers")
app.include_router(rankings_router, prefix="/api/rankings")

# ─── 🩺 Health Check ─────────────────────────────────
@app.get("/")
async def read_root(request: Request):
    block_local_requests_in_prod(request)
    return {"message": "Backend is up and running!"}