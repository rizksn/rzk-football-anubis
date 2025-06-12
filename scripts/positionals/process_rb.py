import argparse
import json
from pathlib import Path
from anubis.utils.normalize.name import normalize_name_for_display
from anubis.utils.normalize.team import normalize_team
from anubis.utils.normalize.player import normalize_player_fields
from anubis.utils.parse.stat_value import convert_stat_value
from anubis.ingest.utils.match_players import match_player_by_name
from anubis.utils.stats.utils import pad_missing_stats

# File paths
SLEEPER_PATH = Path("anubis/data/processed/sleeper/sleeper_players_processed.json")
RUSHING_PATH = Path("anubis/data/processed/nfl/nfl_player_rushing_{year}.processed.json")
RECEIVING_PATH = Path("anubis/data/processed/nfl/nfl_player_receiving_{year}.processed.json")
PASSING_PATH = Path("anubis/data/processed/nfl/nfl_player_passing_{year}.processed.json")
OUT_PATH = Path("anubis/data/processed/nfl/nfl_player_rb_{year}.processed.json")

# Raw stat field mappings by source type
PASS_MAP = {
    "yds": "pass_yds",
    "yds/att": "pass_yds_att",
    "att": "pass_att",
    "cmp": "pass_cmp",
    "cmp_%": "pass_cmp_percent",  
    "td": "pass_td",
    "int": "pass_int",
    "rate": "pass_rate",
    "1st": "pass_first",
    "1st%": "pass_first_percent",
    "20+": "pass_20_plus",
    "40+": "pass_40_plus",
    "lng": "pass_long",
    "sck": "pass_sck",
    "scky": "pass_scky",
}

RUSH_MAP = {
    "att": "rush_att",
    "rush_yds": "rush_yds",  
    "td": "rush_td",
    "20+": "rush_20_plus",
    "40+": "rush_40_plus",
    "lng": "rush_long",
    "rush_1st": "rush_first",
    "rush_1st%": "rush_first_percent",
    "rush_fum": "rush_fum",
}

REC_MAP = {
    "rec": "rec",
    "yds": "rec_yds",
    "td": "rec_td",
    "20+": "rec_20_plus",
    "40+": "rec_40_plus",
    "lng": "rec_long",
    "rec_1st": "rec_first",
    "1st%": "rec_first_percent",
    "rec_fum": "rec_fum",
    "rec_yac/r": "rec_yac_per_rec",
    "tgts": "rec_targets",
}

# All possible final keys
ALL_STAT_KEYS = set(PASS_MAP.values()) | set(RUSH_MAP.values()) | set(REC_MAP.values())

def process_rb_stats(year: int):
    with SLEEPER_PATH.open("r") as f:
        sleeper_pool = json.load(f)

    rushing_data = _load_stat_json(RUSHING_PATH.with_name(RUSHING_PATH.name.format(year=year)))
    receiving_data = _load_stat_json(RECEIVING_PATH.with_name(RECEIVING_PATH.name.format(year=year)))
    passing_data = _load_stat_json(PASSING_PATH.with_name(PASSING_PATH.name.format(year=year)))

    merged = {}

    for source_data, mapping in [
        (rushing_data, RUSH_MAP),
        (receiving_data, REC_MAP),
        (passing_data, PASS_MAP),
    ]:
        for player in source_data:
            raw_name = player["full_name"]
            match = match_player_by_name(raw_name, sleeper_pool)
            if not match or match["position"] != "RB":
                continue

            pid = match["player_id"]
            if pid not in merged:
                merged[pid] = {
                    "player_id": pid,
                    "full_name": normalize_name_for_display(raw_name),
                    "search_full_name": match["search_full_name"],
                    "first_name": match["first_name"],
                    "last_name": match["last_name"],
                    "team": normalize_team(match["team"]),
                    "position": match["position"],
                }

            for k, v in player.items():
                if k in mapping:
                    final_key = mapping[k]
                    merged[pid][final_key] = convert_stat_value(k, v)

    final = [
        pad_missing_stats(normalize_player_fields(p), ALL_STAT_KEYS)
        for p in merged.values()
    ]

    output_path = OUT_PATH.with_name(OUT_PATH.name.format(year=year))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        json.dump(final, f, indent=2)

    print(f"✅ Processed {len(final)} RBs → {output_path.name}")


def _load_stat_json(path: Path):
    if not path.exists():
        return []
    with path.open("r") as f:
        return json.load(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate combined RB stats for a given season")
    parser.add_argument("--year", type=int, required=True, help="Season year (e.g. 2024)")
    args = parser.parse_args()
    process_rb_stats(args.year)