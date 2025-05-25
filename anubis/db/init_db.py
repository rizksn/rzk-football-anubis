from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import asyncio, os
from dotenv import load_dotenv

# Schema-level metadata (each file has its own)
from anubis.db.schemas.core import metadata as core_metadata
from anubis.db.schemas.nfl.nfl_player_passing_2024 import metadata as passing_metadata
from anubis.db.schemas.nfl.nfl_player_rushing_2024 import metadata as rushing_metadata
from anubis.db.schemas.nfl.nfl_player_receiving_2024 import metadata as receiving_metadata
from anubis.db.schemas.nfl.nfl_player_kicking_2024 import metadata as kicking_metadata

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def init():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS core"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS nfl"))

        await conn.run_sync(core_metadata.create_all)
        await conn.run_sync(passing_metadata.create_all)
        await conn.run_sync(rushing_metadata.create_all)
        await conn.run_sync(receiving_metadata.create_all)
        await conn.run_sync(kicking_metadata.create_all)

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init())