import argparse
import json
from pathlib import Path
from anubis.utils.normalize.team import normalize_team  
from anubis.utils.normalize.name import normalize_name_for_display

def process_adp_files(format_filter=None):
    raw_path = Path("anubis/data/raw/draftsharks")
    out_path = Path("anubis/data/processed/draftsharks")

    for format_folder in raw_path.iterdir():
        if not format_folder.is_dir():
            continue

        if format_filter and format_folder.name.lower() != format_filter.lower():
            continue

        processed_format_dir = out_path / format_folder.name
        processed_format_dir.mkdir(parents=True, exist_ok=True)

        for file in format_folder.glob("*.raw.json"):
            with file.open("r") as f:
                data = json.load(f)

            clean_data = []
            for p in data.get("data", []):
                if all(k in p for k in ["name", "position", "team", "adp"]):
                    p["team"] = normalize_team(p["team"])  
                    p["name"] = normalize_name_for_display(p["name"])
                    clean_data.append(p)

            out_file = processed_format_dir / file.name.replace(".raw.json", ".processed.json")
            with out_file.open("w") as f:
                json.dump({"data": clean_data}, f, indent=2)

            print(f"✅ Processed {len(clean_data)} players → {out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process DraftSharks ADP data")
    parser.add_argument("--format", type=str, help="Limit processing to a specific format (e.g., redraft, best ball, dynasty)")
    args = parser.parse_args()

    process_adp_files(format_filter=args.format)