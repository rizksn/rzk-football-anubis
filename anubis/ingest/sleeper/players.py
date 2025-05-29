import json
from pathlib import Path
from sqlalchemy import insert
from anubis.db.base import async_session
from anubis.db.schemas.core.players import players
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert

PROCESSED_PATH = Path("anubis/data/processed/sleeper/sleeper_players_processed.json")

def parse_height(val):
    try:
        if isinstance(val, str) and "'" in val:
            feet, inches = val.replace('"', '').split("'")
            return int(feet) * 12 + int(inches)
        elif isinstance(val, str) and val.strip().isdigit():
            return int(val.strip())
        elif isinstance(val, int):
            return val
    except Exception:
        return None

async def load_sleeper_players():
    with PROCESSED_PATH.open("r") as f:
        data = json.load(f)

    INT_FIELDS = {"depth_chart_order", "height", "weight", "age", "years_exp"}

    for d in data:
        # Convert fantasy_positions list to comma-separated string
        if isinstance(d.get("fantasy_positions"), list):
            d["fantasy_positions"] = ",".join(p.strip() for p in d["fantasy_positions"])
        
        # Clean up optional integer fields
        for field in INT_FIELDS:
            val = d.get(field)
            if field == "height":
                d[field] = parse_height(val)
            elif isinstance(val, str) and val.strip().isdigit():
                d[field] = int(val.strip())
            elif val in (None, ""):
                d[field] = None

        # Convert string birth_date to datetime.date
        birth_date = d.get("birth_date")
        if isinstance(birth_date, str):
            try:
                d["birth_date"] = datetime.strptime(birth_date.strip(), "%Y-%m-%d").date()
            except ValueError:
                d["birth_date"] = None

    async with async_session() as session:
        async with session.begin():
            stmt = insert(players).values(data).on_conflict_do_nothing()
            await session.execute(stmt)

    print(f"✅ Inserted {len(data)} Sleeper players into DB")

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_sleeper_players())