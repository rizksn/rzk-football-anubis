import asyncio
import sys
import os

# Fix path so it can import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from anubis.ingest.nfl.season_rushing import load_rb_data

async def main():
    print("🚀 Ingesting NFL rushing stats...")
    await load_rb_data()
    print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(main())