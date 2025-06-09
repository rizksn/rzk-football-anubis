import json
from pathlib import Path
from datetime import datetime
from anubis.utils.normalize.name import normalize_name_for_display

raw_path = Path("anubis/data/raw/sleeper/sleeper_players_full.json")
out_path = Path("anubis/data/processed/sleeper/sleeper_players_processed.json")

KEEP_FIELDS = {
    "player_id",
    "full_name",
    "search_full_name",
    "college",
    "active",
    "height",
    "number",
    "depth_chart_position",
    "fantasy_positions",
    "years_exp",
    "last_name",
    "weight",
    "age",
    "team",
    "birth_date",
    "first_name",
    "position",
    "depth_chart_order"
}

def calculate_age_years(birth_date_str: str) -> float | None:
    try:
        dob = datetime.strptime(birth_date_str, "%Y-%m-%d")
        today = datetime.today()
        delta = today - dob
        return round(delta.days / 365.25, 1)  # One decimal place
    except Exception:
        return None

def convert_numeric_fields(player: dict):
    for key in ["height", "weight"]:
        if key in player and isinstance(player[key], str) and player[key].isdigit():
            player[key] = int(player[key])
    if "birth_date" in player and player["birth_date"]:
        player["age_years"] = calculate_age_years(player["birth_date"])

def process_players():
    with raw_path.open("r") as f:
        all_players = json.load(f)

    cleaned = []

    for pid, player in all_players.items():
        if player.get("status") != "Active":
            continue

        slimmed = {k: v for k, v in player.items() if k in KEEP_FIELDS}
        from anubis.utils.normalize.team import normalize_team
        slimmed["team"] = normalize_team(slimmed.get("team"))

        slimmed["player_id"] = pid
        slimmed["full_name"] = normalize_name_for_display(slimmed.get("full_name", ""))
        convert_numeric_fields(slimmed)
        cleaned.append(slimmed)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Processed {len(cleaned)} active players → {out_path}")

if __name__ == "__main__":
    process_players()