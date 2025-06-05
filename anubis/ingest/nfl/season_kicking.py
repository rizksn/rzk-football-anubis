import json
import os
import logging
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from anubis.db.base import engine
from anubis.db.schemas.nfl.nfl_player_kicking_2024 import nfl_player_kicking_2024
from anubis.ingest.utils.match_players import match_player_by_name

# ✅ Logger setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ✅ DB session
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# ✅ Helper: safely convert types
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

# ✅ Mapping logic for a single kicker record
def parse_kicker_record(record, player_id):
    return {
        "player_id": player_id,
        "name": record["player"],
        "fgm": to_int(record["fgm"]),
        "fga": to_int(record["att"]),
        "fg_percent": to_float(record["fg_percent"]),
        "fg_1_19": record.get("fg_1_19_>_"),
        "fg_20_29": record.get("fg_20_29_>_"),
        "fg_30_39": record.get("fg_30_39_>_"),
        "fg_40_49": record.get("fg_40_49_>_"),
        "fg_50_59": record.get("fg_50_59_>_"),
        "fg_60_plus": record.get("fg_60_plus_>_"),
        "fg_long": to_int(record["lng"]),
        "fg_blocked": to_int(record["fg_blocked"]),
    }

# ✅ Load and ingest kicker stats
async def load_kicker_data():
    base_dir = os.path.dirname(__file__)
    stat_path = os.path.abspath(os.path.join(base_dir, "../../data/processed/player_stats/nfl_player_kicking_2024.processed.json"))
    sleeper_path = os.path.abspath(os.path.join(base_dir, "../../data/processed/sleeper/sleeper_players_processed.json"))

    with open(stat_path, "r") as f:
        raw_data = json.load(f)

    with open(sleeper_path, "r") as f:
        player_pool = json.load(f)

    parsed_data = []
    unmatched_players = []

    for record in raw_data:
        player_id = match_player_by_name(record["player"], player_pool)
        if player_id:
            parsed_data.append(parse_kicker_record(record, player_id))
        else:
            unmatched_players.append(record["player"])
            logger.warning(f"❌ Unmatched K: {record['player']}")

    if unmatched_players:
        log_path = os.path.join(base_dir, "../../logs/unmatched_kickers.json")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(unmatched_players, f, indent=2)

    async with async_session() as session:
        await session.execute(insert(nfl_player_kicking_2024), parsed_data)
        await session.commit()
        logger.info(f"✅ Inserted {len(parsed_data)} kicker records into nfl_player_kicking_2024")

# ✅ Run directly
if __name__ == "__main__":
    import asyncio
    asyncio.run(load_kicker_data())