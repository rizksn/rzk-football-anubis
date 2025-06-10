import json
import os
import logging
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert as pg_insert

from anubis.db.base import engine
from anubis.db.schemas.nfl.nfl_player_passing_2024 import nfl_player_passing_2024
from anubis.ingest.utils.match_players import match_player_by_name

# Logger setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# DB session
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Type conversion helpers
def to_int(val): return int(val) if val not in ("", "--", None) else None
def to_float(val): return float(val) if val not in ("", "--", None) else None

# Record parser
def parse_passing_record(record, player_id):
    return {
        "player_id": player_id,  
        "search_full_name": record.get("search_full_name", ""),
        "first_name": record.get("first_name", ""),
        "last_name": record.get("last_name", ""),
        "team": record.get("team", "FA"),
        "position": record.get("position", ""),
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

# Main async ingest function
async def load_passing_data():
    base_dir = os.path.dirname(__file__)
    stat_path = os.path.abspath(os.path.join(base_dir, "../../data/processed/nfl/nfl_player_passing_2024.processed.json"))
    sleeper_path = os.path.abspath(os.path.join(base_dir, "../../data/processed/sleeper/sleeper_players_processed.json"))

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
            parsed_data.append(parse_passing_record(record, player_id))
        else:
            unmatched_players.append(raw_name)
            logger.warning(f"❌ Unmatched QB: {raw_name} (normalized: {search_name})")
            logger.debug(f"Record dump: {json.dumps(record, indent=2)}")

    if unmatched_players:
        log_path = os.path.join(base_dir, "../../logs/unmatched_nfl_qbs.json")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(unmatched_players, f, indent=2)

    async with async_session() as session:
        stmt = pg_insert(nfl_player_passing_2024).values(parsed_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=["player_id"],
            set_={c.name: c for c in stmt.excluded if c.name != "player_id"}
        )
        await session.execute(stmt)
        await session.commit()

    logger.info(f"✅ Inserted {len(parsed_data)} QB records into nfl_player_passing_2024")

# Entrypoint
if __name__ == "__main__":
    import asyncio
    asyncio.run(load_passing_data())