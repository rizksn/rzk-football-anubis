import json
import os
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from anubis.db.schemas.nfl.nfl_player_rb_2024 import nfl_player_rb_2024
from anubis.db.base import engine

# ✅ Async session factory
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# ✅ Convert strings to proper types
def parse_rb_record(record):
    return {
        "name": record["name"],
        "rush_yds": int(record["rush_yds"]),
        "att": int(record["att"]),
        "td": int(record["td"]),
        "twenty_plus": int(record["20+"]),             
        "forty_plus": int(record["40+"]),              
        "long": int(record["long"]),
        "rush_1st": int(record["rush_1st"]),
        "rush_1st_percent": float(record["rush_1st%"]), 
        "rush_fum": int(record["rush_fum"]),
    }

# ✅ Main function
async def load_rb_data():
    base_dir = os.path.dirname(__file__)
    json_path = os.path.abspath(os.path.join(base_dir, "../../data/raw/nfl_player_rb_2024.json"))

    with open(json_path, "r") as f:
        raw_data = json.load(f)
        parsed_data = [parse_rb_record(d) for d in raw_data]

    async with async_session() as session:
        await session.execute(insert(nfl_player_rb_2024), parsed_data)
        await session.commit()
        print(f"✅ Inserted {len(parsed_data)} RB records into nfl_player_rb_2024")

# ✅ CLI entry point
if __name__ == "__main__":
    import asyncio
    asyncio.run(load_rb_data())
