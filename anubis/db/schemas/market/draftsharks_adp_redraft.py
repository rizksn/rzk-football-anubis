from sqlalchemy import Table, Column, String, ForeignKey
from anubis.db.schemas.core.players import players  
from anubis.db.schemas.market import market_metadata 

redraft_1qb_0_5_ppr_consensus = Table(
    "redraft_1qb_0_5_ppr_consensus",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)

redraft_1qb_0_5_ppr_sleeper = Table(
    "redraft_1qb_0_5_ppr_sleeper",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)

redraft_1qb_0_5_ppr_yahoo = Table(
    "redraft_1qb_0_5_ppr_yahoo",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)

redraft_1qb_1_ppr_cbs = Table(
    "redraft_1qb_1_ppr_cbs",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)

redraft_1qb_1_ppr_consensus = Table(
    "redraft_1qb_1_ppr_consensus",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)

redraft_1qb_1_ppr_espn = Table(
    "redraft_1qb_1_ppr_espn",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)

redraft_1qb_1_ppr_ffpc = Table(
    "redraft_1qb_1_ppr_ffpc",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)

redraft_1qb_1_ppr_sleeper = Table(
    "redraft_1qb_1_ppr_sleeper",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)

redraft_1qb_non_ppr_cbs = Table(
    "redraft_1qb_non_ppr_cbs",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)

redraft_1qb_non_ppr_consensus = Table(
    "redraft_1qb_non_ppr_consensus",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)

redraft_1qb_non_ppr_sleeper = Table(
    "redraft_1qb_non_ppr_sleeper",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)

redraft_superflex_1_ppr_sleeper = Table(
    "redraft_superflex_1_ppr_sleeper",
    market_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), nullable=True, primary_key=True),
    Column("name", String),
    Column("position", String),
    Column("team", String),
    Column("adp", String),
)