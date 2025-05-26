import json
from pathlib import Path

RAW_PATH = Path("anubis/data/raw/player_stats/nfl_player_passing_2024.json")
OUT_PATH = Path("anubis/data/processed/player_stats/nfl_player_passing_2024.json")

FLOAT_FIELDS = {"yds/att", "cmp_%", "rate", "1st%"}
INT_FIELDS = {
    "pass_yds", "att", "cmp", "td", "int",
    "1st", "20+", "40+", "lng", "sck", "scky"
}

def convert_value(key, value):
    if value in ("", "--"):
        return None
    try:
        if key in INT_FIELDS:
            return int(value.replace(",", ""))
        elif key in FLOAT_FIELDS:
            return float(value.replace("%", "").replace(",", ""))
    except ValueError:
        return value
    return value

def process_passing_stats():
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

    print(f"✅ Processed {len(cleaned)} passing stat lines → {OUT_PATH}")

if __name__ == "__main__":
    process_passing_stats()