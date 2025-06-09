
import asyncio
import logging
import os
import sys
import json
from sqlalchemy import text
from anubis.db.base import async_session

# 🔇 Silence SQL noise
logging.basicConfig(level=logging.WARNING)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.dialects.postgresql.asyncpg").setLevel(logging.WARNING)

RAW_PATH = "anubis/data/raw/sleeper/sleeper_players_full.json"
PROCESSED_PATH = "anubis/data/processed/sleeper/sleeper_players_processed.json"

async def get_db_count():
    async with async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM core.players"))
        return result.scalar()

def get_json_count(path):
    with open(path, "r") as f:
        data = json.load(f)
        if isinstance(data, dict) and "data" in data:
            return len(data["data"])
        return len(data)

async def main():
    raw_count = get_json_count(RAW_PATH)
    processed_count = get_json_count(PROCESSED_PATH)
    db_count = await get_db_count()

    print(f"📦 Raw Sleeper entries:        {raw_count:,}")
    print(f"🧹 Processed active players:  {processed_count:,}")
    print(f"🗃️  Inserted into DB:         {db_count:,}")

    if db_count == processed_count:
        print("\n✅ All processed players successfully ingested!")
    else:
        print("\n⚠️  Mismatch detected — investigate dropped or skipped rows.")

if __name__ == "__main__":
    asyncio.run(main())