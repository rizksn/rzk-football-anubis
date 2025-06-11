from pathlib import Path
import sys

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from anubis.scrapers.draftsharks.all import scrape_all_adp_combinations
from anubis.scrapers.draftsharks.core import run_scraper

if __name__ == "__main__":
    print("🚀 Starting DraftSharks ADP scraping...")
    run_scraper(scrape_all_adp_combinations)