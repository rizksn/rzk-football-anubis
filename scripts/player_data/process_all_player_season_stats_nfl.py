import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.player_data.process_player_season_kicking_stats_nfl import process_kicking_stats
from scripts.player_data.process_player_season_passing_stats_nfl import process_passing_stats
from scripts.player_data.process_player_season_rushing_stats_nfl import process_rushing_stats
from scripts.player_data.process_player_season_receiving_stats_nfl import process_receiving_stats

if __name__ == "__main__":
    print("🔧 Processing all player stat types (kicking, passing, rushing, receiving)...")
    process_kicking_stats()
    process_passing_stats()
    process_rushing_stats()
    process_receiving_stats()
    print("✅ All stats processed and saved to /data/processed/")