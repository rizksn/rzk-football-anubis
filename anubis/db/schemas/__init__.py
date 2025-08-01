from anubis.db.schemas.core.players import players  

from anubis.db.schemas.core.players import core_metadata
from anubis.db.schemas.nfl.nfl_player_passing_2024 import nfl_player_passing_2024
from anubis.db.schemas.nfl.nfl_player_rushing_2024 import nfl_player_rushing_2024
from anubis.db.schemas.nfl.nfl_player_receiving_2024 import nfl_player_receiving_2024
from anubis.db.schemas.nfl.nfl_player_kicking_2024 import nfl_player_kicking_2024
from anubis.db.schemas.nfl.nfl_player_passing_2023 import nfl_player_passing_2023
from anubis.db.schemas.nfl.nfl_player_rushing_2023 import nfl_player_rushing_2023
from anubis.db.schemas.nfl.nfl_player_receiving_2023 import nfl_player_receiving_2023
from anubis.db.schemas.nfl.nfl_player_kicking_2023 import nfl_player_kicking_2023
from anubis.db.schemas.nfl import (
    passing_metadata,
    rushing_metadata,
    receiving_metadata,
    kicking_metadata,
    nfl_player_qb_2024,
    nfl_player_rb_2024,
    nfl_player_wr_2024,
    nfl_player_te_2024,
    nfl_player_qb_2023,
    nfl_player_rb_2023,
    nfl_player_wr_2023,
    nfl_player_te_2023,
)

from anubis.db.schemas.market import market_metadata

__all__ = [
    "core_metadata",
    "nfl_player_passing_2024", "passing_metadata",
    "nfl_player_rushing_2024", "rushing_metadata",
    "nfl_player_receiving_2024", "receiving_metadata",
    "nfl_player_kicking_2024", "kicking_metadata",
    "nfl_player_passing_2023", "passing_metadata",
    "nfl_player_rushing_2023", "rushing_metadata",
    "nfl_player_receiving_2023", "receiving_metadata",
    "nfl_player_kicking_2023", "kicking_metadata",
    "market_metadata",
    "nfl_player_qb_2024",
    "nfl_player_rb_2024",
    "nfl_player_wr_2024",
    "nfl_player_te_2024",
    "nfl_player_qb_2023",
    "nfl_player_rb_2023",
    "nfl_player_wr_2023",
    "nfl_player_te_2023",
    "market_metadata",
]