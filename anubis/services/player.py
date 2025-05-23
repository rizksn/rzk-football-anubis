from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from anubis.db.schemas.nfl.nfl_player_qb_2024 import nfl_player_qb_2024
from anubis.db.schemas.nfl.nfl_player_rb_2024 import nfl_player_rb_2024
from anubis.db.schemas.nfl.nfl_player_wr_2024 import nfl_player_wr_2024
from anubis.db.schemas.nfl.nfl_player_k_2024 import nfl_player_k_2024

POSITION_TABLES = {
    "QB": nfl_player_qb_2024,
    "RB": nfl_player_rb_2024,
    "WR": nfl_player_wr_2024,
    "K": nfl_player_k_2024,
}

async def resolve_nfl_player_id(session: AsyncSession, player: dict) -> int:
    position = player["position"].upper()
    table = POSITION_TABLES.get(position)
    if not table:
        raise ValueError(f"❌ Unknown position: {position}")

    stmt = select(table.c.id).where(
        table.c.name == player["name"],
        table.c.team == player["team"]
    )
    result = await session.execute(stmt)
    player_id = result.scalar_one_or_none()

    if player_id is None:
        raise ValueError(f"❌ Could not resolve ID for {player['name']} ({player['team']} - {position})")

    return player_id