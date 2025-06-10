import json
from pathlib import Path
from anubis.utils.parse.stat_value import convert_stat_value
from anubis.utils.normalize.player import normalize_player_fields
from anubis.utils.normalize.name import normalize_name_for_display
from anubis.ingest.utils.match_players import match_player_by_name

RAW_PATH = Path("anubis/data/raw/nfl/nfl_player_kicking_2024.raw.json")
OUT_PATH = Path("anubis/data/processed/nfl/nfl_player_kicking_2024.processed.json")
SLEEPER_PATH = Path("anubis/data/processed/sleeper/sleeper_players_processed.json")

INT_FIELDS = {"fgm", "att", "lng", "fg_blocked"}
FLOAT_FIELDS = {"fg_percent"}

STRING_FIELDS = {
    "fg_1_19_>_", "fg_20_29_>_", "fg_30_39_>_",
    "fg_40_49_>_", "fg_50_59_>_", "fg_60_plus_>_"
}

def process_kicking_stats():
    # Load raw stat data
    with RAW_PATH.open("r") as f:
        raw_data = json.load(f)

    # Load Sleeper player pool
    with SLEEPER_PATH.open("r") as f:
        sleeper_pool = json.load(f)

    cleaned = []

    for player in raw_data:
        raw_name = player["player"].strip()
        display_name = normalize_name_for_display(raw_name)

        # Match player from Sleeper to backfill metadata
        sleeper_player = match_player_by_name(raw_name, sleeper_pool)

        new_player = {
            "full_name": display_name,
            "search_full_name": sleeper_player["search_full_name"] if sleeper_player else "",
            "first_name": sleeper_player["first_name"] if sleeper_player else "",
            "last_name": sleeper_player["last_name"] if sleeper_player else "",
            "team": sleeper_player["team"] if sleeper_player else "FA",
            "position": sleeper_player["position"] if sleeper_player else ""
        }

        # Convert stat fields
        for k, v in player.items():
            if k == "player":
                continue
            new_player[k] = convert_stat_value(
                k, v,
                int_fields=INT_FIELDS,
                float_fields=FLOAT_FIELDS
            )

        # Normalize height, weight, age, etc.
        new_player = normalize_player_fields(new_player)
        cleaned.append(new_player)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Processed {len(cleaned)} kicker stat lines → {OUT_PATH}")

if __name__ == "__main__":
    process_kicking_stats()