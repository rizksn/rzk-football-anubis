import json
import os
import logging
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from anubis.db.schemas.nfl.nfl_player_receiving_2024 import nfl_player_receiving_2024
from anubis.db.base import engine
from anubis.ingest.utils.match_players import match_player_by_name

from anubis.utils.normalize.name import normalize_name_for_display

# Logger setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# DB session
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Type-safe converters
def to_int(val): return int(val) if val not in ("", "--", None) else None
def to_float(val): return float(val) if val not in ("", "--", None) else None

# Record parser
def parse_wr_record(record, player_id):
    return {
        "player_id": player_id,
        "name": record["player"],
        "rec": to_int(record["rec"]),
        "yds": to_int(record["yds"]),
        "td": to_int(record["td"]),
        "twenty_plus": to_int(record["20+"]),
        "forty_plus": to_int(record["40+"]),
        "long": to_int(record["lng"]),
        "rec_1st": to_int(record["rec_1st"]),
        "first_percent": to_float(record["1st%"]),
        "rec_fum": to_int(record["rec_fum"]),
        "rec_yac_per_rec": to_float(record["rec_yac/r"]),
        "tgts": to_int(record["tgts"]),
    }

# Load and insert WR stats
async def load_wr_data():
    base_dir = os.path.dirname(__file__)

    # Load processed receiving stats
    stat_path = os.path.abspath(os.path.join(base_dir, "../../data/processed/nfl/nfl_player_receiving_2024.processed.json"))
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
            parsed_data.append(parse_wr_record(record, player_id))
        else:
            unmatched_players.append(record["player"])
            logger.warning(f"❌ Unmatched WR: {record['player']}")

    if unmatched_players:
        log_path = os.path.join(base_dir, "../../logs/unmatched_receivers.json")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(unmatched_players, f, indent=2)

    async with async_session() as session:
        await session.execute(insert(nfl_player_receiving_2024), parsed_data)
        await session.commit()
        logger.info(f"✅ Inserted {len(parsed_data)} WR records into nfl_player_receiving_2024")

# Run directly
if __name__ == "__main__":
    import asyncio
    asyncio.run(load_wr_data())