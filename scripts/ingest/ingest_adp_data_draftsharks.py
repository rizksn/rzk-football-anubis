import sys
import os
import asyncio
from sqlalchemy import text
from anubis.db.base import engine

# Fix path so script can run standalone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anubis.ingest.adp.redraft import load_redraft_adp
from anubis.ingest.adp.dynasty import load_dynasty_adp
from anubis.ingest.adp.rookie import load_rookie_adp
from anubis.ingest.adp.bestball import load_bestball_adp

async def ensure_adp_schema_exists():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS adp"))

async def ingest_all_adp():
    print("🚀 Ingesting DraftSharks Redraft ADP...")
    await load_redraft_adp()

    print("🚀 Ingesting DraftSharks Dynasty ADP...")
    await load_dynasty_adp()

    print("🚀 Ingesting DraftSharks Rookie ADP...")
    await load_rookie_adp()

    print("🚀 Ingesting DraftSharks Best Ball ADP...")
    await load_bestball_adp()

    print("✅ All DraftSharks ADP data ingested!")

async def main():
    await ensure_adp_schema_exists()
    await ingest_all_adp()

if __name__ == "__main__":
    asyncio.run(main())