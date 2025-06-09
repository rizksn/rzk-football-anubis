
import subprocess
import sys
import time
from pathlib import Path

PIPELINE_STEPS = [
    ("sleeper", "Sleeper: Fetch players", "sleeper/fetch_players_sleeper.py"),
    ("sleeper", "Sleeper: Process players", "sleeper/process_players_sleeper.py"),
    ("sleeper", "Core: Ingest players", "ingest/core/ingest_players_sleeper.py"),

    ("nfl", "NFL: Fetch raw stats", "nfl/fetch_player_season_stats_nfl.py"),
    ("nfl", "NFL: Process all stats", "nfl/process_all_player_season_stats_nfl.py"),
    ("nfl", "NFL: Ingest all stats", "ingest/nfl/ingest_all_player_season_stats_nfl.py"),

    ("draftsharks", "DraftSharks: Fetch ADP", "draftsharks/fetch_adp_draftsharks.py"),
    ("draftsharks", "DraftSharks: Process ADP", "draftsharks/process_adp_draftsharks.py"),
    ("draftsharks", "DraftSharks: Ingest ADP", "ingest/market/ingest_adp_draftsharks.py"),
]

# Use absolute path of current script directory no matter how it's called
SCRIPTS_DIR = Path(__file__).resolve().parent

def run_script(label, script_name):
    print(f"\n🚀 Starting: {label}")
    script_path = SCRIPTS_DIR / script_name
    start = time.time()
    try:
        subprocess.run(["python", str(script_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {label}")
        sys.exit(e.returncode)
    print(f"✅ Finished: {label} in {round(time.time() - start, 2)}s")

def main():
    args = set(arg.lower() for arg in sys.argv[1:])
    valid_args = {"sleeper", "nfl", "draftsharks"}

    if args and not args.issubset(valid_args):
        print(f"❌ Invalid argument(s): {args - valid_args}")
        print("Usage: python run_pipeline.py [sleeper nfl draftsharks]")
        sys.exit(1)

    selected = args or {"sleeper", "nfl", "draftsharks"}
    print(f"🧠 Running pipeline for: {', '.join(selected)}\n")

    for tag, label, script_name in PIPELINE_STEPS:
        if tag in selected:
            run_script(label, script_name)

    print("\n🎉 Selected pipeline steps completed successfully!")

if __name__ == "__main__":
    main()