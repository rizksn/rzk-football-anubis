import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from anubis.ingest.nfl.season_receiving import load_receiving_data

async def main():
    print("🚀 Ingesting NFL receiving stats...")
    await load_receiving_data()
    print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(main())