# ─── 📦 Standard Library ─────────────────────────────
import os

# ─── 🔧 Third-party ──────────────────────────────────
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ─── 📡 Environment ──────────────────────────────────
ENV = os.getenv("ENV", "development").lower()
IS_DEV = ENV == "development"
print(f"🚀 Starting FastAPI in {ENV.upper()} mode")

# ─── ⚙️ App Setup ─────────────────────────────────────
app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if IS_DEV else [
        "https://rzkfootball.com",
        "https://rzk-anubis.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── 📁 Routers ──────────────────────────────────────
from anubis.routes import auth as auth_routes
from anubis.routes.players import router as players_router
from anubis.routes.simulate import router as simulate_router
from anubis.routes.player_data import router as player_data_router
from anubis.routes.stripe import router as stripe_router

ROUTERS = [
    players_router,
    simulate_router,
    player_data_router,
    stripe_router,
    auth_routes.router,
]

for router in ROUTERS:
    app.include_router(router)

# ─── 🩺 Health Check ─────────────────────────────────
@app.get("/")
def read_root():
    return {"message": "Backend is up and running!"}
