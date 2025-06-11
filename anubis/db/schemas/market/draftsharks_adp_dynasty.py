from sqlalchemy import Table, Column, String, ForeignKey
from anubis.db.schemas.core.players import players
from anubis.db.schemas.market import market_metadata

dynasty_1qb_1_ppr_sleeper = Table(
    "dynasty_1qb_1_ppr_sleeper",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("full_name", String),
    Column("search_full_name", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("team", String),
    Column("position", String),
    Column("adp", String),
    Column("scoring", String),
    Column("platform", String),
    Column("type", String),
)

dynasty_superflex_1_ppr_sleeper = Table(
    "dynasty_superflex_1_ppr_sleeper",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("full_name", String),
    Column("search_full_name", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("team", String),
    Column("position", String),
    Column("adp", String),
    Column("scoring", String),
    Column("platform", String),
    Column("type", String),
)