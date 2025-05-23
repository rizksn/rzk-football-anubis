import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from anubis.db.schemas import metadata
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def init():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS nfl"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS adp"))
        await conn.run_sync(metadata.create_all)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init())