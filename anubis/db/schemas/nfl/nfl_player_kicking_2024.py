from anubis.db.schemas.core.players import players 
from sqlalchemy import Table, Column, Integer, String, Float, MetaData, ForeignKey

metadata = MetaData(schema="nfl")

nfl_player_kicking_2024 = Table(
    "nfl_player_kicking_2024",
    metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), primary_key=True),
    Column("name", String, nullable=False),
    Column("fgm", Integer),
    Column("fga", Integer),
    Column("fg_percent", Float),
    Column("fg_1_19", String),
    Column("fg_20_29", String),
    Column("fg_30_39", String),
    Column("fg_40_49", String),
    Column("fg_50_59", String),
    Column("fg_60_plus", String),
    Column("fg_long", Integer),
    Column("fg_blocked", Integer),
)