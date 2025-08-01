import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from anubis.ingest.nfl.season_passing import load_passing_data

async def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2024  
    print(f"🚀 Ingesting NFL passing stats for {year}...")
    await load_passing_data(year)
    print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(main())
