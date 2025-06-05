import json
import os
import logging
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from anubis.db.schemas.nfl.nfl_player_passing_2024 import nfl_player_passing_2024
from anubis.db.base import engine
from anubis.ingest.utils.match_players import match_player_by_name

# ✅ Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ✅ DB session
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# ✅ Safe casting helpers
def to_int(val): return int(val) if val not in ("", "--", None) else None
def to_float(val): return float(val) if val not in ("", "--", None) else None

# ✅ Convert one QB record into schema-ready format
def parse_qb_record(record, player_id):
    return {
        "player_id": player_id,
        "name": record["player"],
        "pass_yds": to_int(record["pass_yds"]),
        "yds_att": to_float(record["yds/att"]),
        "att": to_int(record["att"]),
        "cmp": to_int(record["cmp"]),
        "cmp_percent": to_float(record["cmp_%"]),
        "td": to_int(record["td"]),
        "int": to_int(record["int"]),
        "rate": to_float(record["rate"]),
        "first": to_int(record["1st"]),
        "first_percent": to_float(record["1st%"]),
        "twenty_plus": to_int(record["20+"]),
        "forty_plus": to_int(record["40+"]),
        "long": to_int(record["lng"]),
        "sck": to_int(record["sck"]),
        "scky": to_int(record["scky"]),
    }

# ✅ Load and ingest passing stats
async def load_qb_data():
    base_dir = os.path.dirname(__file__)

    # Load processed QB stats
    json_path = os.path.abspath(os.path.join(base_dir, "../../data/processed/player_stats/nfl_player_passing_2024.processed.json"))
    with open(json_path, "r") as f:
        raw_data = json.load(f)

    # Load processed Sleeper players
    sleeper_path = os.path.abspath(os.path.join(base_dir, "../../data/processed/sleeper/sleeper_players_processed.json"))
    with open(sleeper_path, "r") as f:
        player_pool = json.load(f)

    parsed_data = []
    unmatched_players = []

    for record in raw_data:
        player_id = match_player_by_name(record["player"], player_pool)
        if player_id:
            parsed_data.append(parse_qb_record(record, player_id))
        else:
            unmatched_players.append(record["player"])
            logger.warning(f"❌ Unmatched QB: {record['player']}")

    if unmatched_players:
        log_path = os.path.join(base_dir, "../../logs/unmatched_qbs.json")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(unmatched_players, f, indent=2)

    async with async_session() as session:
        await session.execute(insert(nfl_player_passing_2024), parsed_data)
        await session.commit()
        logger.info(f"✅ Inserted {len(parsed_data)} QB records into nfl_player_passing_2024")

# ✅ Run if direct
if __name__ == "__main__":
    import asyncio
    asyncio.run(load_qb_data())