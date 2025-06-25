import argparse
import json
from pathlib import Path
from anubis.utils.normalize.name import normalize_name_for_display, normalize_name_for_matching
from anubis.utils.normalize.team import normalize_team
from anubis.ingest.utils.match_players import match_player_by_name
from anubis.utils.logging.unmatched_logger import log_unmatched_player
from anubis.scrapers.draftsharks.utils import normalize_segment

RAW_DIR = Path("anubis/data/raw/draftsharks")
OUT_DIR = Path("anubis/data/processed/draftsharks")
SLEEPER_PATH = Path("anubis/data/processed/sleeper/sleeper_players_processed.json")

def extract_field(filename: str, index: int) -> str:
    # Handles any stray `-` or space in file names just in case
    base = filename.replace(".raw.json", "")
    parts = normalize_segment(base).split("_")
    if index >= len(parts):
        raise ValueError(f"Invalid filename format: {filename}")
    return parts[index]

def process_adp_files(format_filter=None):
    with SLEEPER_PATH.open("r") as f:
        sleeper_pool = json.load(f)

    for format_folder in RAW_DIR.iterdir():
        if not format_folder.is_dir():
            continue

        if format_filter and format_folder.name.lower() != format_filter.lower():
            continue

        processed_dir = OUT_DIR / normalize_segment(format_folder.name)
        processed_dir.mkdir(parents=True, exist_ok=True)

        for file in format_folder.glob("*.raw.json"):
            with file.open("r") as f:
                raw_json = json.load(f)

            clean_data = []
            ordered_players = raw_json.get("data", [])
            table_name = file.name.replace(".raw.json", "")

            for i, p in enumerate(ordered_players):
                raw_name = p.get("name")
                if not raw_name or not all(k in p for k in ["team", "position", "adp"]):
                    continue

                normalized_name = normalize_name_for_matching(raw_name)
                display_name = normalize_name_for_display(raw_name)
                sleeper_player = match_player_by_name(raw_name, sleeper_pool)

                if not sleeper_player:
                    position = p["position"].lower()
                    log_path = f"logs/unmatched/adp/draftsharks_processing_{position}.json"

                    log_unmatched_player(
                        log_path=log_path,
                        player_data={
                            "name": raw_name,
                            "normalized": normalized_name,
                            "team": normalize_team(p["team"]),
                            "position": p["position"],
                            "table": table_name
                        }
                    )
                    continue

                enriched_player = {
                    "player_id": sleeper_player["player_id"],
                    "full_name": sleeper_player["full_name"],
                    "search_full_name": sleeper_player["search_full_name"],
                    "first_name": sleeper_player["first_name"],
                    "last_name": sleeper_player["last_name"],
                    "team": normalize_team(sleeper_player["team"]),
                    "position": sleeper_player["position"],
                    "rank": p["rank"],
                    "adp": str(p["adp"]).strip(),
                    "scoring": extract_field(file.name, 2),
                    "platform": extract_field(file.name, 3),
                    "type": extract_field(file.name, 1)
                }

                clean_data.append(enriched_player)

            out_file = processed_dir / file.name.replace(".raw.json", ".processed.json")
            with out_file.open("w") as f:
                json.dump({"data": clean_data}, f, indent=2)

            print(f"✅ Processed {len(clean_data)} players → {out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process DraftSharks ADP data")
    parser.add_argument("--format", type=str, help="Limit processing to a specific format (e.g., redraft, best ball, dynasty)")
    args = parser.parse_args()

    process_adp_files(format_filter=args.format)
