import asyncio
import logging
import os
import sys

# Suppress SQLAlchemy logging noise for both sync + async engines
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.dialects.postgresql.asyncpg").setLevel(logging.WARNING)

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from anubis.ingest.nfl.season_passing import load_qb_data
from anubis.ingest.nfl.season_receiving import load_wr_data
from anubis.ingest.nfl.season_rushing import load_rb_data
from anubis.ingest.nfl.season_kicking import load_kicker_data


async def main():
    print("🚀 Starting full NFL player stats ingestion...\n")

    try:
        await load_qb_data()
    except Exception as e:
        print(f"❌ Failed to load QB data: {e}")

    try:
        await load_wr_data()
    except Exception as e:
        print(f"❌ Failed to load WR data: {e}")

    try:
        await load_rb_data()
    except Exception as e:
        print(f"❌ Failed to load RB data: {e}")

    try:
        await load_kicker_data()
    except Exception as e:
        print(f"❌ Failed to load Kicker data: {e}")

    print("\n✅ All NFL season stat tables successfully ingested.")


if __name__ == "__main__":
    asyncio.run(main())