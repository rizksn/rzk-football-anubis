import json
import os
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from anubis.db.schemas.nfl.nfl_player_k_2024 import nfl_player_k_2024
from anubis.db.base import engine

# Session
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Parsing
def parse_kicker_record(record):
    def to_int(value):
        try:
            return int(value)
        except:
            return None

    def to_float(value):
        try:
            return float(value)
        except:
            return None

    return {
        "name": record["player"],
        "fgm": to_int(record["fgm"]),
        "fga": to_int(record["att"]),
        "fg_percent": to_float(record["fg_percent"]),
        "fg_1_19": record["fg_1_19_>_"],
        "fg_20_29": record["fg_20_29_>_"],
        "fg_30_39": record["fg_30_39_>_"],
        "fg_40_49": record["fg_40_49_>_"],
        "fg_50_59": record["fg_50_59_>_"],
        "fg_60_plus": record["fg_60_plus_>_"],
        "fg_long": to_int(record["lng"]),
        "fg_blocked": to_int(record["fg_blocked"]),
    }

# Load
async def load_kicker_data():
    base_dir = os.path.dirname(__file__)
    json_path = os.path.abspath(os.path.join(base_dir, "../../data/raw/nfl_player_fg_2024.json"))

    with open(json_path, "r") as f:
        raw_data = json.load(f)
        parsed_data = [parse_kicker_record(d) for d in raw_data]

    async with async_session() as session:
        await session.execute(insert(nfl_player_k_2024), parsed_data)
        await session.commit()
        print(f"✅ Inserted {len(parsed_data)} kicker records into nfl_player_k_2024")

# Run
if __name__ == "__main__":
    import asyncio
    asyncio.run(load_kicker_data())