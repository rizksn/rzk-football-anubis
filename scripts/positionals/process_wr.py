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
RECEIVING_PATH = Path("anubis/data/processed/nfl/nfl_player_receiving_{year}.processed.json")
PASSING_PATH = Path("anubis/data/processed/nfl/nfl_player_passing_{year}.processed.json")
RUSHING_PATH = Path("anubis/data/processed/nfl/nfl_player_rushing_{year}.processed.json")
OUT_PATH = Path("anubis/data/processed/nfl/nfl_player_wr_{year}.processed.json")

# Relevant stat fields
REC_FIELDS = {"rec", "yds", "td", "20+", "40+", "lng", "rec_1st", "1st%", "rec_fum", "rec_yac/r", "tgts"}
PASS_FIELDS = {"cmp", "att", "td", "int"}
RUSH_FIELDS = {"att", "rush_yds", "td", "20+", "40+", "long", "rush_1st", "rush_1st%", "rush_fum"}

def process_wr_stats(year: int):
    with SLEEPER_PATH.open("r") as f:
        sleeper_pool = json.load(f)

    receiving_data = _load_stat_json(RECEIVING_PATH.with_name(RECEIVING_PATH.name.format(year=year)))
    passing_data = _load_stat_json(PASSING_PATH.with_name(PASSING_PATH.name.format(year=year)))
    rushing_data = _load_stat_json(RUSHING_PATH.with_name(RUSHING_PATH.name.format(year=year)))

    merged = {}

    for source_data, fields in [
        (receiving_data, REC_FIELDS),
        (passing_data, PASS_FIELDS),
        (rushing_data, RUSH_FIELDS),
    ]:
        for player in source_data:
            raw_name = player["player"]
            match = match_player_by_name(raw_name, sleeper_pool)
            if not match or match["position"] != "WR":
                continue

            pid = match["player_id"]
            if pid not in merged:
                merged[pid] = {
                    "player_id": match["player_id"],
                    "full_name": normalize_name_for_display(raw_name),
                    "search_full_name": match["search_full_name"],
                    "first_name": match["first_name"],
                    "last_name": match["last_name"],
                    "team": normalize_team(match["team"]),
                    "position": match["position"]
                }

            for k in fields:
                if k in player:
                    merged[pid][k] = convert_stat_value(k, player[k])

    final = [normalize_player_fields(p) for p in merged.values()]
    OUT_PATH.with_name(OUT_PATH.name.format(year=year)).parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.with_name(OUT_PATH.name.format(year=year)).open("w") as f:
        json.dump(final, f, indent=2)

    print(f"✅ Processed {len(final)} WRs → {OUT_PATH.name.format(year=year)}")


def _load_stat_json(path: Path):
    if not path.exists():
        return []
    with path.open("r") as f:
        return json.load(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate combined WR stats for a given season")
    parser.add_argument("--year", type=int, required=True, help="Season year (e.g. 2024)")
    args = parser.parse_args()
    process_wr_stats(args.year)