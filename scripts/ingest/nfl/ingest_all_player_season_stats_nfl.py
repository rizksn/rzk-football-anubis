import asyncio
import logging
import os
import sys

# Suppress SQLAlchemy logging noise for both sync + async engines
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.dialects.postgresql.asyncpg").setLevel(logging.WARNING)

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from anubis.ingest.nfl.season_passing import load_passing_data
from anubis.ingest.nfl.season_receiving import load_receiving_data
from anubis.ingest.nfl.season_rushing import load_rushing_data
from anubis.ingest.nfl.season_kicking import load_kicker_data


async def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2024  # 👈 Get year from CLI arg
    print(f"🚀 Starting NFL stats ingestion for {year}...\n")

    try:
        await load_passing_data(year)
    except Exception as e:
        print(f"❌ Failed to load QB data: {e}")

    try:
        await load_receiving_data(year)
    except Exception as e:
        print(f"❌ Failed to load WR data: {e}")

    try:
        await load_rushing_data(year)
    except Exception as e:
        print(f"❌ Failed to load RB data: {e}")

    try:
        await load_kicker_data(year)
    except Exception as e:
        print(f"❌ Failed to load Kicker data: {e}")

    print(f"\n✅ All NFL stats for {year} successfully ingested.")

# ✅ ADD THIS:
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
