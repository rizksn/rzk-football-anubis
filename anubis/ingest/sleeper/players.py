import json
from pathlib import Path
from sqlalchemy import insert
from anubis.db.base import async_session
from anubis.db.schemas.core.players import players  

PROCESSED_PATH = Path("anubis/data/processed/sleeper/sleeper_players_processed.json")

async def load_sleeper_players():
    with PROCESSED_PATH.open("r") as f:
        data = json.load(f)

    async with async_session() as session:
        async with session.begin():
            await session.execute(insert(players), data)

        print(f"✅ Inserted {len(data)} Sleeper players into DB")