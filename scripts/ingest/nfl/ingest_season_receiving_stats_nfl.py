import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from anubis.ingest.nfl.receiving import load_wr_data

async def main():
    print("🚀 Ingesting NFL receiving stats...")
    await load_wr_data()
    print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(main())