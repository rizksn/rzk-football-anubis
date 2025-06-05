# scripts/ingest/ingest_season_kicking_stats_nfl.py

import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from anubis.ingest.nfl.season_kicking import load_kicker_data

async def main():
    print("🚀 Ingesting NFL kicking stats...")
    await load_kicker_data()
    print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(main())