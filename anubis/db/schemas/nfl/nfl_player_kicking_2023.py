from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from anubis.db.schemas.core.players import players
from anubis.db.schemas.nfl import kicking_metadata

nfl_player_kicking_2023 = Table(
    "nfl_player_kicking_2023",
    kicking_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), primary_key=True),
    Column("search_full_name", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("team", String),
    Column("position", String),
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
