import os
import json
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from anubis.db.base import engine
from anubis.db.schemas.adp.draftsharks_rookie_2025 import draftsharks_rookie_2025
from anubis.services.player import resolve_nfl_player_id  
from .utils import parse_metadata, get_json_files

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def load_rookie_adp():
    base_path = os.path.join(os.path.dirname(__file__), "../../data/raw/adp/draftsharks/rookie")
    files = get_json_files(base_path)

    async with async_session() as session:
        for file in files:
            meta = parse_metadata(file)
            with open(os.path.join(base_path, file)) as f:
                raw = json.load(f)["data"]
                records = []
                for player in raw:
                    try:
                        player_id = await resolve_nfl_player_id(session, player)
                        record = {
                            "player_id": player_id,
                            "name": player["name"],
                            "team": player["team"],
                            "position": player["position"],
                            "adp": float(player["adp"]),
                            "scoring": meta["scoring"],
                            "platform": meta["platform"],
                            "type": meta["type"]
                        }
                        records.append(record)
                    except Exception as e:
                        print(f"⚠️ Skipped {player['name']}: {e}")

                await session.execute(insert(draftsharks_rookie_2025), records)
                print(f"✅ Inserted {len(records)} from {file}")
        await session.commit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_rookie_adp())