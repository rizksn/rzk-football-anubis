from pathlib import Path
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert as pg_insert

from anubis.db.base import engine
import anubis.db.schemas.market.draftsharks_adp_redraft as redraft_tables
import anubis.db.schemas.market.draftsharks_adp_dynasty as dynasty_tables
import anubis.db.schemas.market.draftsharks_adp_rookie as rookie_tables
import anubis.db.schemas.market.draftsharks_adp_bestball as bestball_tables

from anubis.ingest.utils.utils import parse_metadata, get_json_files

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

FORMAT_TO_TABLE = {
    "redraft": redraft_tables,
    "dynasty": dynasty_tables,
    "rookie": rookie_tables,
    "best_ball": bestball_tables,
}

BASE_DIR = Path(__file__).resolve().parent / "../../data/processed/draftsharks"
BASE_DIR = BASE_DIR.resolve()  # normalize the path

def normalize_table_key(meta: dict, format_name: str) -> str:
    key = f"{format_name}_{meta['type']}_{meta['scoring']}_{meta['platform']}".lower()
    key = key.replace(" ", "_").replace("-", "_")
    key = key.replace("0.5", "0_5") 
    key = key.replace("1.0", "1")    
    return key

async def load_all_draftsharks_adp():
    async with async_session() as session:
        for format_name, format_module in FORMAT_TO_TABLE.items():
            format_path = BASE_DIR / format_name
            files = get_json_files(format_path)

            for file in files:
                meta = parse_metadata(file)
                table_key = normalize_table_key(meta, format_name)
                table = getattr(format_module, table_key, None)

                if table is None:
                    print(f"❌ No matching table found for key: {table_key} (from file: {file})")
                    continue

                with open(format_path / file) as f:
                    raw = json.load(f)["data"]
                    records = []

                    for player in raw:
                        try:
                            if not isinstance(player, dict):
                                print(f"❌ Skipping malformed entry (not a dict): {player}")
                                continue

                            record = {
                                "player_id": player["player_id"],
                                "full_name": player["full_name"],
                                "search_full_name": player["search_full_name"],
                                "first_name": player["first_name"],
                                "last_name": player["last_name"],
                                "team": player["team"],
                                "position": player["position"],
                                "adp": str(player["adp"]).strip(),
                                "scoring": player["scoring"],
                                "platform": player["platform"],
                                "type": player["type"]
                            }
                            records.append(record)

                        except Exception as e:
                            name = player["name"] if isinstance(player, dict) and "name" in player else str(player)
                            print(f"⚠️ Skipped {name}: {e}")
                            print(f"📄 Processing file: {file}")

                    valid_records = [r for r in records if r.get("player_id")]
                    if not valid_records:
                        print(f"⚠️ No valid records to insert from {file}")
                    else:
                        stmt = pg_insert(table).values(valid_records)
                        stmt = stmt.on_conflict_do_update(
                            index_elements=["player_id"],
                            set_={col: getattr(stmt.excluded, col) for col in [
                                "full_name", "search_full_name", "first_name", "last_name",
                                "team", "position", "adp", "scoring", "platform", "type"
                            ]}
                        )
                        await session.execute(stmt)
                        print(f"✅ Inserted {len(valid_records)} from {file}")

        await session.commit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_all_draftsharks_adp())