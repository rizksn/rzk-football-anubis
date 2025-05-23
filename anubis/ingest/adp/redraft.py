import os
import json
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from anubis.db.base import engine
from anubis.db.schemas.adp.draftsharks_redraft_2025 import draftsharks_redraft_2025

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

def parse_metadata(filename: str):
    # e.g. redraft_1qb_0.5-ppr_sleeper.json
    parts = filename.replace(".json", "").split("_")
    return {
        "format": parts[0],  # redraft
        "type": parts[1].upper(),  # 1QB or SUPERFLEX
        "scoring": parts[2].replace("-", " ").upper(),  # 0.5 PPR
        "platform": parts[3].capitalize()  # Sleeper
    }

def parse_players(data, meta):
    return [
        {
            "player_id": p["id"],
            "name": p["name"],
            "team": p["team"],
            "position": p["position"],
            "adp": float(p["adp"]),
            "scoring": meta["scoring"],
            "platform": meta["platform"],
            "type": meta["type"]
        }
        for p in data
    ]

async def load_redraft_adp():
    base_path = os.path.join(os.path.dirname(__file__), "../../data/raw/adp/draftsharks/redraft")
    files = [f for f in os.listdir(base_path) if f.endswith(".json")]

    async with async_session() as session:
        for file in files:
            meta = parse_metadata(file)
            with open(os.path.join(base_path, file)) as f:
                raw = json.load(f)["data"]
                records = parse_players(raw, meta)
                await session.execute(insert(draftsharks_redraft_2025), records)
                print(f"✅ Inserted {len(records)} from {file}")
        await session.commit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_redraft_adp())