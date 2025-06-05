import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

# Explicit table imports to register FKs
from anubis.db.schemas.core.players import players
from anubis.db.schemas.nfl.nfl_player_passing_2024 import nfl_player_passing_2024
from anubis.db.schemas.nfl.nfl_player_rushing_2024 import nfl_player_rushing_2024
from anubis.db.schemas.nfl.nfl_player_receiving_2024 import nfl_player_receiving_2024
from anubis.db.schemas.nfl.nfl_player_kicking_2024 import nfl_player_kicking_2024

# Import shared metadata objects
from anubis.db.schemas import (
    core_metadata,
    passing_metadata,
    rushing_metadata,
    receiving_metadata,
    kicking_metadata,
)

# Load env vars
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG_SQL = os.getenv("DEBUG_SQL", "False") == "True"

# Optional debug checks
print("✅ core_metadata.tables:", list(core_metadata.tables.keys()))
print("✅ passing_metadata.tables:", list(passing_metadata.tables.keys()))
print("✅ players.metadata is core_metadata:", players.metadata is core_metadata)

assert "core.players" in core_metadata.tables
assert players.metadata is core_metadata

async def init():
    engine = create_async_engine(DATABASE_URL, echo=DEBUG_SQL)

    # Step 1: Ensure schemas exist
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS core"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS nfl"))

    # Step 2: Create all tables together for proper FK resolution
    async with engine.begin() as conn:
        def sync_create_all(sync_conn):
            all_tables = (
                list(core_metadata.tables.values())
                + list(passing_metadata.tables.values())
                + list(rushing_metadata.tables.values())
                + list(receiving_metadata.tables.values())
                + list(kicking_metadata.tables.values())
            )
            for table in all_tables:
                print(f"✅ Creating table: {table.schema}.{table.name}")
            from sqlalchemy import MetaData
            tmp = MetaData()
            tmp._schemas = {"core", "nfl"}  # Register schemas manually
            for table in all_tables:
                table.to_metadata(tmp)  # ✅ updated here
            tmp.create_all(sync_conn)

        await conn.run_sync(sync_create_all)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init())