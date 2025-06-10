import json
from pathlib import Path
from anubis.utils.parse.stat_value import convert_stat_value
from anubis.utils.normalize.name import (
    normalize_name_for_display,
    normalize_name_for_matching
)
from anubis.utils.normalize.player import normalize_player_fields
from anubis.ingest.utils.match_players import match_player_by_name

RAW_PATH = Path("anubis/data/raw/nfl/nfl_player_rushing_2024.raw.json")
OUT_PATH = Path("anubis/data/processed/nfl/nfl_player_rushing_2024.processed.json")
SLEEPER_PATH = Path("anubis/data/processed/sleeper/sleeper_players_processed.json")

FLOAT_FIELDS = {"rush_1st%"}
INT_FIELDS = {
    "rush_yds", "att", "td", "20+", "40+", "lng",
    "rush_1st", "rush_fum"
}

def process_rushing_stats():
    with RAW_PATH.open("r") as f:
        raw_data = json.load(f)

    with SLEEPER_PATH.open("r") as f:
        sleeper_pool = json.load(f)

    cleaned = []

    for player in raw_data:
        raw_name = player["player"].strip()
        display_name = normalize_name_for_display(raw_name)
        search_name = normalize_name_for_matching(raw_name)

        sleeper_player = match_player_by_name(search_name, sleeper_pool)

        new_player = {
            "player_id": sleeper_player["player_id"] if sleeper_player else "",
            "full_name": display_name,
            "search_full_name": sleeper_player["search_full_name"] if sleeper_player else search_name,
            "first_name": sleeper_player["first_name"] if sleeper_player else "",
            "last_name": sleeper_player["last_name"] if sleeper_player else "",
            "team": sleeper_player["team"] if sleeper_player else "FA",
            "position": sleeper_player["position"] if sleeper_player else ""
        }

        for k, v in player.items():
            if k == "player":
                continue
            new_player[k] = convert_stat_value(
                k, v,
                int_fields=INT_FIELDS,
                float_fields=FLOAT_FIELDS
            )

        new_player = normalize_player_fields(new_player)
        cleaned.append(new_player)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Processed {len(cleaned)} rushing stat lines → {OUT_PATH}")

if __name__ == "__main__":
    process_rushing_stats()