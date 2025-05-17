import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add backend/anubis to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "anubis")))

# Route imports
from anubis.routes.players import router as players_router
from anubis.routes.simulate import router as simulate_router
from anubis.routes.player_data import router as player_data_router  

app = FastAPI()

# CORS setup
ENV = os.getenv("ENV", "development")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if ENV == "development" else ["https://app.rzkfootball.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(players_router)
app.include_router(simulate_router)
app.include_router(player_data_router)  

@app.get("/")
def read_root():
    """Health check endpoint for backend"""
    return {"message": "Backend is up and running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))