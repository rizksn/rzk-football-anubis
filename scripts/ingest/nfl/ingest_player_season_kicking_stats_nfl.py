import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from anubis.ingest.nfl.season_kicking import load_kicker_data

async def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2024  
    print(f"🚀 Ingesting NFL kicking stats for {year}...")
    await load_kicker_data(year)
    print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(main())
