import argparse
import json
from pathlib import Path
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert as pg_insert

from anubis.db.base import engine
from anubis.db.schemas.nfl.nfl_player_qb_2024 import nfl_player_qb_2024
from anubis.db.schemas.nfl.nfl_player_rb_2024 import nfl_player_rb_2024
from anubis.db.schemas.nfl.nfl_player_wr_2024 import nfl_player_wr_2024
from anubis.db.schemas.nfl.nfl_player_te_2024 import nfl_player_te_2024
from anubis.db.schemas.nfl.nfl_player_kicking_2024 import nfl_player_kicking_2024
from anubis.utils.parse.stat_value import convert_stat_value

# Map position to SQLAlchemy table
POSITION_TABLES = {
    "qb": nfl_player_qb_2024,
    "rb": nfl_player_rb_2024,
    "wr": nfl_player_wr_2024,
    "te": nfl_player_te_2024,
}

DATA_DIR = Path("anubis/data/processed/nfl")
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

def get_file_for_position(pos: str, year: int) -> Path:
    return DATA_DIR / f"nfl_player_{pos}_{year}.processed.json"

async def ingest_positional_stats(year: int):
    async with async_session() as session:
        for pos, table in POSITION_TABLES.items():
            path = get_file_for_position(pos, year)
            if not path.exists():
                print(f"⚠️ Skipping {pos.upper()}: {path.name} not found")
                continue

            with path.open("r") as f:
                players = json.load(f)

            if not players:
                print(f"⚠️ No data found for {pos.upper()} in {path.name}")
                continue

            valid_columns = {col.name for col in inspect(table).columns}
            clean_players = []

            for p in players:
                filtered = {}
                for k in valid_columns:
                    raw_val = p.get(k)
                    val = convert_stat_value(k, raw_val)

                    if val is None:
                        col_type = inspect(table).c[k].type.__class__.__name__.lower()
                        if "int" in col_type or "float" in col_type or "numeric" in col_type:
                            val = 0
                        else:
                            val = None  # explicitly set to null for non-numeric

                    filtered[k] = val
                clean_players.append(filtered)

            if not clean_players:
                print(f"❌ No valid data to insert for {pos.upper()}")
                continue

            stmt = pg_insert(table).values(clean_players)
            stmt = stmt.on_conflict_do_update(
                index_elements=["player_id"],
                set_={col: getattr(stmt.excluded, col) for col in clean_players[0] if col != "player_id"}
            )

            await session.execute(stmt)
            print(f"✅ Inserted {len(clean_players)} {pos.upper()} rows → {table.name}")

        await session.commit()
        print("🎉 Done ingesting positional tables.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest positional NFL player tables into the DB")
    parser.add_argument("--year", type=int, required=True, help="Season year (e.g. 2024)")
    args = parser.parse_args()

    import asyncio
    asyncio.run(ingest_positional_stats(args.year))