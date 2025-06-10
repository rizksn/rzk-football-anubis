import json
from pathlib import Path
from anubis.utils.normalize.player import normalize_player_fields

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
    "depth_chart_order",
}

def process_players():
    with raw_path.open("r") as f:
        all_players = json.load(f)

    cleaned = []

    for pid, player in all_players.items():
        if player.get("status") != "Active":
            continue

        slimmed = {k: v for k, v in player.items() if k in KEEP_FIELDS}
        slimmed["player_id"] = pid

        normalized = normalize_player_fields(slimmed)

        cleaned.append(normalized)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(cleaned, f, indent=2)

    print(f"✅ Processed {len(cleaned)} active players → {out_path}")

if __name__ == "__main__":
    process_players()