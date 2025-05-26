import os
from anubis.scrapers.nfl.config import POSITION_ABBREV

def get_stat_output_path(stat_type: str, year: int, root: str = None) -> str:
    if not root:
        root = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "player_stats")
    abbrev = POSITION_ABBREV[stat_type]
    return os.path.abspath(os.path.join(root, f"nfl_player_{abbrev}_{year}.json"))