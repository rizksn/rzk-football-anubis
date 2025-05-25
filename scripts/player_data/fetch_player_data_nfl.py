import sys
import os
import json
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from anubis.scrapers.nfl_stats import fetch_nfl_stats

if __name__ == "__main__":
    print("📡 Scraping NFL player stats...")
    asyncio.run(fetch_nfl_stats(stat_type="rushing", year=2024))