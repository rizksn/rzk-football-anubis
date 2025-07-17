from pathlib import Path
import json

def load_adp_data(adp_key: str) -> list:
    """Load ADP data from processed ADP formats across all league types."""
    if adp_key.startswith("redraft_"):
        league_format = "redraft"
    elif adp_key.startswith("dynasty_"):
        league_format = "dynasty"
    elif adp_key.startswith("rookie_"):
        league_format = "rookie"
    elif adp_key.startswith("best_ball_"):
        league_format = "best_ball"
    else:
        raise ValueError(f"Unknown league format in ADP key: {adp_key}")

    path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "processed"
        / "draftsharks"
        / league_format
        / f"{adp_key}.processed.json"
    )

    print("🔍 Loading:", path)

    if not path.exists():
        raise FileNotFoundError(f"ADP file not found: {path}")

    with open(path, "r") as f:
        return json.load(f)["data"]
    

def create_empty_draft_board(total_teams: int, rounds: int) -> list:
    """Create an empty draft board grid."""
    total_picks = total_teams * rounds
    return [[None] for _ in range(total_picks)]
