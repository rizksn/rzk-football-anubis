import logging
import os
import sys
import asyncio

# 💣 Fully suppress SQLAlchemy logging
logging.basicConfig(level=logging.WARNING)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.dialects.postgresql.asyncpg").setLevel(logging.WARNING)

# Optional: suppress asyncio debug noise
logging.getLogger("asyncio").setLevel(logging.WARNING)

# Project path fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from anubis.ingest.core.players import load_sleeper_players

async def main():
    print("🚀 Ingesting Sleeper players into DB...")
    await load_sleeper_players()
    print("✅ Done.")

if __name__ == "__main__":
    asyncio.run(main())