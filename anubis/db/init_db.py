from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import asyncio, os
from dotenv import load_dotenv

from anubis.db.schemas import (
    core_metadata,
    passing_metadata,
    rushing_metadata,
    receiving_metadata,
    kicking_metadata,
)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG_SQL = os.getenv("DEBUG_SQL", "False") == "True"

async def init():
    engine = create_async_engine(DATABASE_URL, echo=DEBUG_SQL)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS core"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS nfl"))
        
        for metadata in [core_metadata, passing_metadata, rushing_metadata, receiving_metadata, kicking_metadata]:
            await conn.run_sync(metadata.create_all)

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init())