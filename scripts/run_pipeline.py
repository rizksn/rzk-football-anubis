import subprocess
import sys
import time
from pathlib import Path

# 📦 Pipeline steps mapped by tag
PIPELINE_STEPS = [
    # Sleeper pipeline
    ("sleeper", "Sleeper: Fetch players", "sleeper/fetch_players_sleeper.py"),
    ("sleeper", "Sleeper: Process players", "sleeper/process_players_sleeper.py"),
    ("sleeper", "Core: Ingest players", "ingest/core/ingest_players_sleeper.py"),

    # NFL raw stats
    ("nfl", "NFL: Fetch raw stats", ["nfl/fetch_player_season_stats_nfl.py", "--all"]),
    ("nfl", "NFL: Process all stats", "nfl/process_all_player_season_stats_nfl.py"),
    ("nfl", "NFL: Ingest all stats", "ingest/nfl/ingest_all_player_season_stats_nfl.py"),

    # Positional table processors
    ("positional", "NFL: Process RBs", ["positionals/process_rb.py", "--year", "2024"]),
    ("positional", "NFL: Process WRs", ["positionals/process_wr.py", "--year", "2024"]),
    ("positional", "NFL: Process TEs", ["positionals/process_te.py", "--year", "2024"]),
    ("positional", "NFL: Process QBs", ["positionals/process_qb.py", "--year", "2024"]),

    # Ingest positional tables (after processors above)
    ("positional", "NFL: Ingest positional stats", ["ingest/nfl/ingest_positional_table_stats.py", "--year", "2024"]),

    # DraftSharks ADP
    ("draftsharks", "DraftSharks: Fetch ADP", "draftsharks/fetch_adp_draftsharks.py"),
    ("draftsharks", "DraftSharks: Process ADP", "draftsharks/process_adp_draftsharks.py"),
    ("draftsharks", "DraftSharks: Ingest ADP", "ingest/market/ingest_adp_draftsharks.py"),
]

# 📁 Use absolute path of script dir regardless of how script is invoked
SCRIPTS_DIR = Path(__file__).resolve().parent

def run_script(label, script_entry):
    print(f"\n🚀 Starting: {label}")
    if isinstance(script_entry, list):
        script_path = [str(SCRIPTS_DIR / script_entry[0])] + script_entry[1:]
    else:
        script_path = [str(SCRIPTS_DIR / script_entry)]
    
    start = time.time()
    try:
        subprocess.run(["python"] + script_path, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {label}")
        sys.exit(e.returncode)
    print(f"✅ Finished: {label} in {round(time.time() - start, 2)}s")

def main():
    args = set(arg.lower() for arg in sys.argv[1:])
    valid_args = {"sleeper", "nfl", "draftsharks", "positional"}

    if args and not args.issubset(valid_args):
        print(f"❌ Invalid argument(s): {args - valid_args}")
        print("Usage: python run_pipeline.py [sleeper nfl draftsharks positional]")
        sys.exit(1)

    selected = args or {"sleeper", "nfl", "draftsharks", "positional"}
    print(f"🧠 Running pipeline for: {', '.join(selected)}\n")

    for tag, label, script_name in PIPELINE_STEPS:
        if tag in selected:
            run_script(label, script_name)

    print("\n🎉 Selected pipeline steps completed successfully!")

if __name__ == "__main__":
    main()