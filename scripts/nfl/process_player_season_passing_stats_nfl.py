import json
from pathlib import Path
from anubis.utils.parse.stat_value import convert_stat_value

RAW_PATH = Path("anubis/data/raw/nfl/nfl_player_passing_2024.raw.json")
OUT_PATH = Path("anubis/data/processed/nfl/nfl_player_passing_2024.processed.json")

FLOAT_FIELDS = {"yds/att", "cmp_%", "rate", "1st%"}
INT_FIELDS = {
    "pass_yds", "att", "cmp", "td", "int",
    "1st", "20+", "40+", "lng", "sck", "scky"
}

def process_passing_stats():
    with RAW_PATH.open("r") as f:
        raw_data = json.load(f)

    cleaned = []

    for player in raw_data:
        new_player = {"player": player["player"].strip()}
        for k, v in player.items():
            if k == "player":
                continue
            new_player[k] = convert_stat_value(
                k, v,
                int_fields=INT_FIELDS,
                float_fields=FLOAT_FIELDS
            )
        cleaned.append(new_player)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Processed {len(cleaned)} passing stat lines → {OUT_PATH}")

if __name__ == "__main__":
    process_passing_stats()