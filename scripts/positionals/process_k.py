import argparse
import json
from pathlib import Path
from anubis.utils.normalize.name import normalize_name_for_display
from anubis.utils.normalize.team import normalize_team
from anubis.utils.normalize.player import normalize_player_fields
from anubis.utils.parse.stat_value import convert_stat_value
from anubis.ingest.utils.match_players import match_player_by_name

# File paths
SLEEPER_PATH = Path("anubis/data/processed/sleeper/sleeper_players_processed.json")
KICKING_PATH = Path("anubis/data/processed/nfl/nfl_player_kicking_{year}.processed.json")
OUT_PATH = Path("anubis/data/processed/nfl/nfl_player_k_{year}.processed.json")

# Fields specific to kickers
KICK_FIELDS = {
    "fgm", "fga", "fg%", "fg_long", "xpm", "xpa", "xp%"
}

def process_k_stats(year: int):
    with SLEEPER_PATH.open("r") as f:
        sleeper_pool = json.load(f)

    kicking_data = _load_stat_json(KICKING_PATH.with_name(KICKING_PATH.name.format(year=year)))
    merged = {}

    for player in kicking_data:
        raw_name = player["player"]
        match = match_player_by_name(raw_name, sleeper_pool)
        if not match or match["position"] != "K":
            continue

        pid = match["player_id"]
        merged[pid] = {
            "player_id": match["player_id"],
            "full_name": normalize_name_for_display(raw_name),
            "search_full_name": match["search_full_name"],
            "first_name": match["first_name"],
            "last_name": match["last_name"],
            "team": normalize_team(match["team"]),
            "position": match["position"]
        }

        for k in KICK_FIELDS:
            if k in player:
                merged[pid][k] = convert_stat_value(k, player[k])

    final = [normalize_player_fields(p) for p in merged.values()]
    OUT_PATH.with_name(OUT_PATH.name.format(year=year)).parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.with_name(OUT_PATH.name.format(year=year)).open("w") as f:
        json.dump(final, f, indent=2)

    print(f"✅ Processed {len(final)} Ks → {OUT_PATH.name.format(year=year)}")


def _load_stat_json(path: Path):
    if not path.exists():
        return []
    with path.open("r") as f:
        return json.load(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate combined K stats for a given season")
    parser.add_argument("--year", type=int, required=True, help="Season year (e.g. 2024)")
    args = parser.parse_args()
    process_k_stats(args.year)