import json
import os
import logging
import importlib
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert as pg_insert

from anubis.db.base import engine
from anubis.ingest.utils.match_players import match_player_by_name

# Logger setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# DB session
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Safe converters
def to_int(val): return int(val) if val not in ("", "--", None) else None
def to_float(val): return float(val) if val not in ("", "--", None) else None

# Record parser
def parse_kicker_record(record, player_id):
    return {
        "player_id": player_id,
        "search_full_name": record.get("search_full_name", ""),
        "first_name": record.get("first_name", ""),
        "last_name": record.get("last_name", ""),
        "team": record.get("team", "FA"),
        "position": record.get("position", ""),
        "fgm": to_int(record.get("fgm")),
        "fga": to_int(record.get("att")),
        "fg_percent": to_float(record.get("fg_percent")),
        "fg_1_19": record.get("fg_1_19_>_"),
        "fg_20_29": record.get("fg_20_29_>_"),
        "fg_30_39": record.get("fg_30_39_>_"),
        "fg_40_49": record.get("fg_40_49_>_"),
        "fg_50_59": record.get("fg_50_59_>_"),
        "fg_60_plus": record.get("fg_60_plus_>_"),
        "fg_long": to_int(record.get("lng")),
        "fg_blocked": to_int(record.get("fg_blocked")),
    }

# Main ingest function
async def load_kicker_data(year: int = 2024):
    base_dir = os.path.dirname(__file__)
    stat_path = os.path.abspath(os.path.join(
        base_dir, f"../../data/processed/nfl/nfl_player_kicking_{year}.processed.json"
    ))
    sleeper_path = os.path.abspath(os.path.join(
        base_dir, "../../data/processed/sleeper/sleeper_players_processed.json"
    ))

    # Dynamically import the correct schema
    table_module = importlib.import_module(f"anubis.db.schemas.nfl.nfl_player_kicking_{year}")
    kicking_table = getattr(table_module, f"nfl_player_kicking_{year}")

    with open(stat_path, "r") as f:
        raw_data = json.load(f)
    with open(sleeper_path, "r") as f:
        player_pool = json.load(f)

    parsed_data = []
    unmatched_players = []

    for record in raw_data:
        raw_name = record.get("player") or record.get("full_name") or "<unknown>"
        search_name = record.get("search_full_name")

        player_obj = match_player_by_name(search_name, player_pool)
        if player_obj:
            player_id = player_obj["player_id"]
            parsed_data.append(parse_kicker_record(record, player_id))
        else:
            unmatched_players.append(raw_name)
            logger.warning(f"❌ Unmatched K: {raw_name} (normalized: {search_name})")
            logger.debug(f"Record dump: {json.dumps(record, indent=2)}")

    if unmatched_players:
        log_path = os.path.join(base_dir, f"../../logs/unmatched/unmatched_nfl_k_{year}.json")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(unmatched_players, f, indent=2)

    async with async_session() as session:
        stmt = pg_insert(kicking_table).values(parsed_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=["player_id"],
            set_={c.name: c for c in stmt.excluded if c.name != "player_id"}
        )
        await session.execute(stmt)
        await session.commit()

    logger.info(f"✅ Inserted {len(parsed_data)} kicker records into nfl_player_kicking_{year}")

# Entrypoint
if __name__ == "__main__":
    import asyncio
    asyncio.run(load_kicker_data())
