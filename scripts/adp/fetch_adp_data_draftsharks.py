import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anubis.scrapers.adp.draftsharks.all import scrape_all_adp_combinations

if __name__ == "__main__":
    print("📡 Starting DraftSharks ADP scraping...")
    scrape_all_adp_combinations()