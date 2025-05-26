import json
from pathlib import Path

RAW_PATH = Path("anubis/data/raw/player_stats/nfl_player_receiving_2024.json")
OUT_PATH = Path("anubis/data/processed/player_stats/nfl_player_receiving_2024.json")

FLOAT_FIELDS = {"1st%", }
INT_FIELDS = {
    "rec", "yds", "td", "20+", "40+", "lng",
    "rec_1st", "rec_fum", "rec_yac/r", "tgts"
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

def process_receiving_stats():
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

    print(f"✅ Processed {len(cleaned)} receiving stat lines → {OUT_PATH}")

if __name__ == "__main__":
    process_receiving_stats()