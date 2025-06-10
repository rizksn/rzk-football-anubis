from .team import normalize_team
from datetime import datetime

def calculate_age_years(birth_date_str: str) -> float | None:
    try:
        dob = datetime.strptime(birth_date_str, "%Y-%m-%d")
        today = datetime.today()
        delta = today - dob
        return round(delta.days / 365.25, 1)
    except Exception:
        return None

def convert_numeric_fields(player: dict):
    for key in ["height", "weight"]:
        if key in player and isinstance(player[key], str) and player[key].isdigit():
            player[key] = int(player[key])
    if "birth_date" in player and player["birth_date"]:
        player["age_years"] = calculate_age_years(player["birth_date"])

def normalize_player_fields(player: dict) -> dict:
    player["first_name"] = player.get("first_name", "").strip()
    player["last_name"] = player.get("last_name", "").strip()
    player["team"] = normalize_team(player.get("team"))
    player["position"] = (player.get("position") or "").strip().upper()
    if isinstance(player.get("fantasy_positions"), list):
        player["fantasy_positions"] = [
            pos.strip().upper() for pos in player["fantasy_positions"]
        ]
    convert_numeric_fields(player)
    return player