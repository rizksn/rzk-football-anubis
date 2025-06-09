import os
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert as pg_insert

from anubis.db.base import engine
from anubis.services.player import resolve_nfl_player_id
import anubis.db.schemas.market.draftsharks_adp_redraft as redraft_tables
import anubis.db.schemas.market.draftsharks_adp_dynasty as dynasty_tables
import anubis.db.schemas.market.draftsharks_adp_rookie as rookie_tables
import anubis.db.schemas.market.draftsharks_adp_bestball as bestball_tables

from anubis.ingest.utils.utils import parse_metadata, get_json_files
from anubis.utils.normalize.name import normalize_name_for_display

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

FORMAT_TO_TABLE = {
    "redraft": redraft_tables,
    "dynasty": dynasty_tables,
    "rookie": rookie_tables,
    "best_ball": bestball_tables,
}

BASE_DIR = os.path.join(os.path.dirname(__file__), "../../data/processed/draftsharks")

def normalize_table_key(meta: dict, format_name: str) -> str:
    return (
        f"{format_name}_{meta['type']}_{meta['scoring']}_{meta['platform']}"
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

async def load_all_draftsharks_adp():
    async with async_session() as session:
        for format_name, format_module in FORMAT_TO_TABLE.items():
            format_path = os.path.join(BASE_DIR, format_name)
            files = get_json_files(format_path)

            for file in files:
                meta = parse_metadata(file)
                table_key = normalize_table_key(meta, format_name)
                table = getattr(format_module, table_key, None)

                if table is None:
                    print(f"❌ No matching table found for key: {table_key} (from file: {file})")
                    continue

                with open(os.path.join(format_path, file)) as f:
                    raw = json.load(f)["data"]
                    records = []

                    for player in raw:
                        try:
                            if not isinstance(player, dict):
                                print(f"❌ Skipping malformed entry (not a dict): {player}")
                                continue

                            player_id = await resolve_nfl_player_id(session, player)

                            record = {
                                "player_id": player_id,
                                "name": normalize_name_for_display(player["name"]),
                                "team": player["team"],
                                "position": player["position"],
                                "adp": str(player["adp"]),
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
                        from sqlalchemy.dialects.postgresql import insert as pg_insert

                        stmt = pg_insert(table).values(valid_records)
                        stmt = stmt.on_conflict_do_update(
                            index_elements=["player_id"],  # this matches your PK constraint
                            set_={
                                "name": stmt.excluded.name,
                                "team": stmt.excluded.team,
                                "position": stmt.excluded.position,
                                "adp": stmt.excluded.adp,
                            },
                        )
                        await session.execute(stmt)

                        print(f"✅ Inserted {len(valid_records)} from {file}")

        await session.commit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_all_draftsharks_adp())