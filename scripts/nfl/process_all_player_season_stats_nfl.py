import sys
import os
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.nfl.process_player_season_kicking_stats_nfl import process_kicking_stats
from scripts.nfl.process_player_season_passing_stats_nfl import process_passing_stats
from scripts.nfl.process_player_season_rushing_stats_nfl import process_rushing_stats
from scripts.nfl.process_player_season_receiving_stats_nfl import process_receiving_stats

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2024)
    args = parser.parse_args()

    print(f"🔧 Processing all player stat types for {args.year} (kicking, passing, rushing, receiving)...")
    process_kicking_stats(args.year)
    process_passing_stats(args.year)
    process_rushing_stats(args.year)
    process_receiving_stats(args.year)
    print("✅ All stats processed and saved to /data/processed/")
