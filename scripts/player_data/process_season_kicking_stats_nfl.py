# scripts/player_data/process_season_kicking_stats_nfl.py

import json
from pathlib import Path

RAW_PATH = Path("anubis/data/raw/player_stats/nfl_player_kicking_2024.json")
OUT_PATH = Path("anubis/data/processed/player_stats/nfl_player_kicking_2024.json")

INT_FIELDS = {"fgm", "att", "lng", "fg_blocked"}
FLOAT_FIELDS = {"fg_percent"}

STRING_FIELDS = {
    "fg_1_19_>_", "fg_20_29_>_", "fg_30_39_>_",
    "fg_40_49_>_", "fg_50_59_>_", "fg_60_plus_>_"
}

def convert_value(key, value):
    if value in ("", "--"):
        return None
    try:
        if key in INT_FIELDS:
            return int(value.replace(",", ""))
        elif key in FLOAT_FIELDS:
            return float(value.replace("%", "").replace(",", ""))
        elif key in STRING_FIELDS:
            return value.strip()
    except ValueError:
        return value
    return value

def process_kicking_stats():
    with RAW_PATH.open("r") as f:
        raw_data = json.load(f)

    cleaned = []
    for player in raw_data:
        new_player = {"player": player["player"].strip()}
        for k, v in player.items():
            if k == "player":
                continue
            new_player[k] = convert_value(k, v)
        cleaned.append(new_player)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Processed {len(cleaned)} kicker stat lines → {OUT_PATH}")

if __name__ == "__main__":
    process_kicking_stats()