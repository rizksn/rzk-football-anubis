from .core import scrape_format, run_scraper

def scrape_redraft(page):
    scrape_format(
        page,
        format_name="Redraft",
        types=["1QB", "Superflex"],
        scorings=["Non-PPR", "0.5 PPR", "1 PPR", "TE Premium"],
        platforms=["Sleeper", "CBS", "Consensus"]
    )

if __name__ == "__main__":
    run_scraper(scrape_redraft)
    