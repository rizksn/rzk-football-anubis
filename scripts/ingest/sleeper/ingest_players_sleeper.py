# scripts/ingest/ingest_players_sleeper.py

import asyncio
import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from anubis.ingest.core.players import load_sleeper_players

async def main():
    print("🚀 Ingesting Sleeper players into DB...")
    await load_sleeper_players()
    print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(main())