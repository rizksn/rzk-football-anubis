import json
import os
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from anubis.db.schemas.nfl.nfl_player_passing_2024 import nfl_player_qb_2024
from anubis.db.base import engine

# ✅ Create async session factory
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# ✅ Convert strings to correct types
def parse_qb_record(record):
    return {
        "name": record["name"],
        "pass_yds": int(record["pass_yds"]),
        "yds_att": float(record["yds_att"]),
        "att": int(record["att"]),
        "cmp": int(record["cmp"]),
        "cmp_percent": float(record["cmp%"]),
        "td": int(record["td"]),
        "int": int(record["int"]),
        "rate": float(record["rate"]),
        "first": int(record["1st"]),
        "first_percent": float(record["1st%"]),
        "twenty_plus": int(record["20+"]),
        "forty_plus": int(record["40+"]),
        "long": int(record["long"]),
        "sck": int(record["sck"]),
        "scky": int(record["scky"]),
    }

# ✅ Main ingestion logic
async def load_qb_data():
    base_dir = os.path.dirname(__file__)
    json_path = os.path.abspath(os.path.join(base_dir, "../../data/raw/nfl_player_qb_2024.json"))

    with open(json_path, "r") as f:
        raw_data = json.load(f)
        parsed_data = [parse_qb_record(d) for d in raw_data]

    async with async_session() as session:
        await session.execute(insert(nfl_player_qb_2024), parsed_data)
        await session.commit()
        print(f"✅ Inserted {len(parsed_data)} QB records into nfl_player_qb_2024")

# ✅ Entry point to run it directly
if __name__ == "__main__":
    import asyncio
    asyncio.run(load_qb_data())