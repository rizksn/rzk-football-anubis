import asyncio
import logging
from sqlalchemy import text

from anubis.db.base import engine
from anubis.ingest.market.load_draftsharks_adp import load_all_draftsharks_adp

# Suppress SQLAlchemy logging noise for both sync + async engines
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.dialects.postgresql.asyncpg").setLevel(logging.WARNING)

async def ensure_market_schema_exists():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS market"))


async def main():
    print("🚀 Ingesting DraftSharks ADP data into DB...")
    await ensure_market_schema_exists()
    await load_all_draftsharks_adp()
    print("✅ Done.")


if __name__ == "__main__":
    asyncio.run(main())