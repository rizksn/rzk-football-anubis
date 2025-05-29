import os

def get_stat_output_path(stat_type: str, year: int, root: str = None) -> str:
    if not root:
        root = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "data", "raw", "player_stats"
        )

    # Normalize filename for consistency
    normalized_type = "kicking" if stat_type == "field-goals" else stat_type

    return os.path.abspath(os.path.join(
        root, f"nfl_player_{normalized_type}_{year}.raw.json"
    ))