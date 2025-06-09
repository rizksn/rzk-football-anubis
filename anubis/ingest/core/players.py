import json
import math
import logging
from pathlib import Path
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert
from anubis.db.base import async_session
from anubis.db.schemas.core.players import players

# 🔇 Full SQLAlchemy logging suppression (both sync and asyncpg)
logging.basicConfig(level=logging.WARNING)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.dialects.postgresql.asyncpg").setLevel(logging.WARNING)

PROCESSED_PATH = Path("anubis/data/processed/sleeper/sleeper_players_processed.json")

def to_float_or_none(value):
    try:
        val = float(value)
        return val if math.isfinite(val) else None  # ✅ Reject NaN, inf, -inf
    except:
        return None

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

async def load_sleeper_players(batch_size: int = 500):
    with PROCESSED_PATH.open("r") as f:
        data = json.load(f)

    INT_FIELDS = {"depth_chart_order", "height", "weight", "age", "years_exp"}
    FLOAT_FIELDS = {"age_years"}

    for d in data:
        if isinstance(d.get("fantasy_positions"), list):
            d["fantasy_positions"] = ",".join(p.strip() for p in d["fantasy_positions"])

        for field in INT_FIELDS:
            val = d.get(field)
            if field == "height":
                d[field] = parse_height(val)
            elif isinstance(val, str) and val.strip().isdigit():
                d[field] = int(val.strip())
            elif val in (None, ""):
                d[field] = None

        birth_date = d.get("birth_date")
        if isinstance(birth_date, str):
            try:
                d["birth_date"] = datetime.strptime(birth_date.strip(), "%Y-%m-%d").date()
            except ValueError:
                d["birth_date"] = None

        for field in FLOAT_FIELDS:
            d[field] = to_float_or_none(d.get(field))

    async with async_session() as session:
        async with session.begin():
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                stmt = insert(players).values(batch).on_conflict_do_nothing()
                await session.execute(stmt)

    print(f"✅ Inserted {len(data)} Sleeper players into DB in batches of {batch_size}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(load_sleeper_players())