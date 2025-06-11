from sqlalchemy import Table, Column, String, ForeignKey
from anubis.db.schemas.core.players import players
from anubis.db.schemas.market import market_metadata

best_ball_1qb_0_5_ppr_underdog = Table(
    "best_ball_1qb_0_5_ppr_underdog",
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

best_ball_1qb_te_premium_ffpc = Table(
    "best_ball_1qb_te_premium_ffpc",
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