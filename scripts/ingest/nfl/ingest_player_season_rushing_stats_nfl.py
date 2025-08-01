import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from anubis.ingest.nfl.season_rushing import load_rushing_data

async def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2024  
    print(f"🚀 Ingesting NFL rushing stats for {year}...")
    await load_rushing_data(year)
    print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(main())
