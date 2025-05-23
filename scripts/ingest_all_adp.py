import sys
import os
import asyncio

# Fix path so script can run standalone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import each loader function
from anubis.ingest.adp.redraft import load_redraft_adp
from anubis.ingest.adp.dynasty import load_dynasty_adp
from anubis.ingest.adp.rookie import load_rookie_adp
from anubis.ingest.adp.bestball import load_bestball_adp

async def ingest_all_adp():
    print("🚀 Ingesting DraftSharks Redraft ADP...")
    await load_redraft_adp()

    print("🚀 Ingesting DraftSharks Dynasty ADP...")
    await load_dynasty_adp()

    print("🚀 Ingesting DraftSharks Rookie ADP...")
    await load_rookie_adp()

    print("🚀 Ingesting DraftSharks Best Ball ADP...")
    await load_bestball_adp()

    print("✅ All DraftSharks ADP data ingested!")

if __name__ == "__main__":
    asyncio.run(ingest_all_adp())