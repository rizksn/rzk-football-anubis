import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anubis.scrapers.draftsharks.all import scrape_all_adp_combinations
from anubis.scrapers.draftsharks.core import run_scraper

if __name__ == "__main__":
    print("🚀 Starting DraftSharks ADP scraping...")
    run_scraper(scrape_all_adp_combinations)  