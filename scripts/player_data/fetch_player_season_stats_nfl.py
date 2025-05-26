import sys
import os
import argparse
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from anubis.scrapers.nfl.fetch_player_season_stats_nfl import fetch_player_season_stats, fetch_all_positions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch NFL season stats")
    parser.add_argument("--stat-type", type=str, default="rushing", help="Stat type: passing, rushing, receiving, field-goals")
    parser.add_argument("--year", type=int, default=2024, help="NFL season year")
    parser.add_argument("--all", action="store_true", help="Scrape all stat types")

    args = parser.parse_args()

    print(f"📡 Scraping NFL stats for {args.stat_type if not args.all else 'ALL TYPES'} ({args.year})...")
    
    if args.all:
        asyncio.run(fetch_all_positions(year=args.year))
    else:
        asyncio.run(fetch_player_season_stats(stat_type=args.stat_type, year=args.year))