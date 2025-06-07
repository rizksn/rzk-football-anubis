import os
import json
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from anubis.db.base import engine
from anubis.services.player import resolve_nfl_player_id
from anubis.db.schemas.market import (
    draftsharks_redraft_2025,
    draftsharks_dynasty_2025,
    draftsharks_rookie_2025,
    draftsharks_bestball_2025,
)
from .utils import parse_metadata, get_json_files

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

FORMAT_TO_TABLE = {
    "redraft": draftsharks_redraft_2025,
    "dynasty": draftsharks_dynasty_2025,
    "rookie": draftsharks_rookie_2025,
    "best_ball": draftsharks_bestball_2025,
}

BASE_DIR = os.path.join(os.path.dirname(__file__), "../../data/processed/draftsharks")

async def load_all_draftsharks_adp():
    async with async_session() as session:
        for format_name, table in FORMAT_TO_TABLE.items():
            format_path = os.path.join(BASE_DIR, format_name)
            files = get_json_files(format_path)

            for file in files:
                meta = parse_metadata(file)
                with open(os.path.join(format_path, file)) as f:
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

                    invalid = [r for r in records if not r.get("player_id")]
                    for r in invalid:
                        print(f"❌ Skipping invalid record (missing player_id): {r.get('name')}")

                    valid_records = [r for r in records if r.get("player_id")]
                    if not valid_records:
                        print(f"⚠️ No valid records to insert from {file}")
                    else:
                        await session.execute(insert(table), valid_records)
                        print(f"✅ Inserted {len(valid_records)} from {file}")

        await session.commit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_all_draftsharks_adp())