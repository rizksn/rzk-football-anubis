# Standard lib
import os
import sys

# Third-party
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Extend Python path (for running from root)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "anubis")))

# Local imports
from anubis.routes import (
    auth as auth_routes,
)
from anubis.routes.players import router as players_router
from anubis.routes.simulate import router as simulate_router
from anubis.routes.player_data import router as player_data_router

# App instance
app = FastAPI()

# CORS
ENV = os.getenv("ENV", "development")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if ENV == "development" else ["https://rzkfootball.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(players_router)
app.include_router(simulate_router)
app.include_router(player_data_router)
app.include_router(auth_routes.router)

# Health check
@app.get("/")
def read_root():
    return {"message": "Backend is up and running!"}