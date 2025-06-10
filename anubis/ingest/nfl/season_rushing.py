import json
import os
import logging
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from anubis.db.schemas.nfl.nfl_player_rushing_2024 import nfl_player_rushing_2024
from anubis.db.base import engine
from anubis.ingest.utils.match_players import match_player_by_name

from anubis.utils.normalize.name import normalize_name_for_display

# Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# DB session
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Safe converters
def to_int(val): return int(val) if val not in ("", "--", None) else None
def to_float(val): return float(val) if val not in ("", "--", None) else None

# Parser
def parse_rushing_record(record, player_id):
    return {
        "player_id": player_id,
        "name": record["player"],
        "rush_yds": to_int(record["rush_yds"]),
        "att": to_int(record["att"]),
        "td": to_int(record["td"]),
        "twenty_plus": to_int(record["20+"]),
        "forty_plus": to_int(record["40+"]),
        "long": to_int(record["lng"]),
        "rush_1st": to_int(record["rush_1st"]),
        "rush_1st_percent": to_float(record["rush_1st%"]),
        "rush_fum": to_int(record["rush_fum"]),
    }

# Ingest logic
async def load_rushing_data():
    base_dir = os.path.dirname(__file__)

    stat_path = os.path.abspath(os.path.join(base_dir, "../../data/processed/nfl/nfl_player_rushing_2024.processed.json"))
    sleeper_path = os.path.abspath(os.path.join(base_dir, "../../data/processed/sleeper/sleeper_players_processed.json"))

    with open(stat_path, "r") as f:
        raw_data = json.load(f)
    with open(sleeper_path, "r") as f:
        player_pool = json.load(f)

    parsed_data = []
    unmatched_players = []

    for record in raw_data:
        normalized_name = normalize_name_for_display(record["player"])
        player_id = match_player_by_name(normalized_name, player_pool)

        if player_id:
            parsed_data.append(parse_rushing_record(record, player_id))
        else:
            unmatched_players.append(record["player"])
            logger.warning(f"❌ Unmatched RB: {record['player']}")

    if unmatched_players:
        log_path = os.path.join(base_dir, "../../logs/unmatched_rbs.json")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(unmatched_players, f, indent=2)

    async with async_session() as session:
        await session.execute(insert(nfl_player_rushing_2024), parsed_data)
        await session.commit()
        logger.info(f"✅ Inserted {len(parsed_data)} RB records into nfl_player_rushing_2024")

# Run if direct
if __name__ == "__main__":
    import asyncio
    asyncio.run(load_rushing_data())