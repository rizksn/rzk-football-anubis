from sqlalchemy import Table, Column, Integer, String, Float
from anubis.db.schemas.base import metadata

nfl_player_k_2024 = Table(
    "nfl_player_k_2024",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("fgm", Integer),
    Column("fga", Integer),
    Column("fg_percent", Float, key="fg%"),
    Column("fg_long", Integer),
    Column("xpm", Integer),
    Column("xpa", Integer),
    Column("xp_percent", Float, key="xp%"),
)