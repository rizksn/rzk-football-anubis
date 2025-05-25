# scripts/process_sleeper_players.py

import json
from pathlib import Path

RAW_PATH = Path("anubis/data/raw/sleeper/sleeper_players_full.json")
OUT_PATH = Path("anubis/data/processed/sleeper/sleeper_players_processed.json")

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

def process_players():
    with RAW_PATH.open("r") as f:
        all_players = json.load(f)

    cleaned = []

    for pid, player in all_players.items():
        if player.get("status") != "Active":
            continue

        slimmed = {
            k: v for k, v in player.items()
            if k in KEEP_FIELDS
        }

        # Always ensure player_id is kept (top-level key)
        slimmed["player_id"] = pid
        cleaned.append(slimmed)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"Processed {len(cleaned)} active players → {OUT_PATH}")

if __name__ == "__main__":
    process_players()