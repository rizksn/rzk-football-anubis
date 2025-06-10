import asyncio
import sys
import os

# Fix path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from anubis.ingest.nfl.season_passing import load_passing_data

async def main():
    print("🚀 Ingesting NFL passing stats...")
    await load_passing_data()
    print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(main())