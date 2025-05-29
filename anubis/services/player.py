import re
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from anubis.db.schemas.nfl.nfl_player_passing_2024 import nfl_player_passing_2024
from anubis.db.schemas.nfl.nfl_player_rushing_2024 import nfl_player_rushing_2024
from anubis.db.schemas.nfl.nfl_player_receiving_2024 import nfl_player_receiving_2024
from anubis.db.schemas.nfl.nfl_player_kicking_2024 import nfl_player_kicking_2024

POSITION_TABLES = {
    "QB": nfl_player_passing_2024,
    "RB": nfl_player_rushing_2024,
    "WR": nfl_player_receiving_2024,
    "K": nfl_player_kicking_2024,
}

def normalize_name_for_matching(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r'\b(jr\.?|sr\.?|iii|ii|iv)\b', '', name)  # remove suffixes
    name = re.sub(r'\s+', ' ', name)  # collapse extra spaces
    return name.strip()

async def resolve_nfl_player_id(session: AsyncSession, player: dict) -> int:
    position = player["position"].upper()
    table = POSITION_TABLES.get(position)
    if not table:
        raise ValueError(f"❌ Unknown position: {position}")

    normalized_name = normalize_name_for_matching(player["name"])
    team = player["team"].strip().lower()

    stmt = select(table.c.id).where(
        func.lower(table.c.team) == team,
        func.lower(func.replace(table.c.name, '.', '')) == normalized_name.replace('.', '')  # handles 'Bijan Robinson Jr.' vs 'Bijan Robinson'
    )

    result = await session.execute(stmt)
    player_id = result.scalar_one_or_none()

    if player_id is None:
        raise ValueError(f"❌ Could not resolve ID for {player['name']} ({player['team']} - {position})")

    return player_id