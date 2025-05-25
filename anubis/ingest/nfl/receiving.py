import json
import os
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from anubis.db.schemas.nfl.nfl_player_receiving_2024 import nfl_player_wr_2024
from anubis.db.base import engine

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

def parse_wr_record(record):
    return {
        "name": record["name"],
        "rec": int(record["rec"]),
        "yds": int(record["yds"]),
        "td": int(record["td"]),
        "twenty_plus": int(record["20+"]),
        "forty_plus": int(record["40+"]),
        "long": int(record["lng"]),
        "rec_1st": int(record["rec_1st"]),
        "first_percent": float(record["1st%"]),
        "rec_fum": int(record["rec_fum"]),
        "rec_yac_per_rec": float(record["rec_yac/r"]),
        "tgts": int(record["tgts"]),
    }

async def load_wr_data():
    base_dir = os.path.dirname(__file__)
    json_path = os.path.abspath(os.path.join(base_dir, "../../data/raw/nfl_player_wr_2024.json"))

    with open(json_path, "r") as f:
        raw_data = json.load(f)
        parsed_data = [parse_wr_record(d) for d in raw_data]

    async with async_session() as session:
        await session.execute(insert(nfl_player_wr_2024), parsed_data)
        await session.commit()
        print(f"✅ Inserted {len(parsed_data)} WR records into nfl_player_wr_2024")

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_wr_data())