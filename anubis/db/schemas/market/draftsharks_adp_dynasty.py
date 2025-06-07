from sqlalchemy import Table, Column, String, ForeignKey
from anubis.db.schemas.core.players import players
from anubis.db.schemas.market import market_metadata

dynasty_1qb_1_ppr_sleeper = Table(
    "dynasty_1qb_1_ppr_sleeper",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)

dynasty_superflex_1_ppr_sleeper = Table(
    "dynasty_superflex_1_ppr_sleeper",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)