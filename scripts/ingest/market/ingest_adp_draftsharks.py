import asyncio
from sqlalchemy import text
from anubis.db.base import engine
from anubis.ingest.market.load_draftsharks_adp import load_all_adp

async def ensure_market_schema_exists():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS market"))

async def main():
    await ensure_market_schema_exists()
    await load_all_adp()

if __name__ == "__main__":
    asyncio.run(main())