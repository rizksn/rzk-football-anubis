# Force early registration of the core.players table so FK resolution succeeds
from anubis.db.schemas.core.players import players  # ensures FK resolution

# Exported metadata objects and table references
from anubis.db.schemas.core.players import core_metadata
from anubis.db.schemas.nfl.nfl_player_passing_2024 import nfl_player_passing_2024
from anubis.db.schemas.nfl.nfl_player_rushing_2024 import nfl_player_rushing_2024
from anubis.db.schemas.nfl.nfl_player_receiving_2024 import nfl_player_receiving_2024
from anubis.db.schemas.nfl.nfl_player_kicking_2024 import nfl_player_kicking_2024
from anubis.db.schemas.nfl import (
    passing_metadata,
    rushing_metadata,
    receiving_metadata,
    kicking_metadata,
)

__all__ = [
    "core_metadata",
    "nfl_player_passing_2024", "passing_metadata",
    "nfl_player_rushing_2024", "rushing_metadata",
    "nfl_player_receiving_2024", "receiving_metadata",
    "nfl_player_kicking_2024", "kicking_metadata",
]