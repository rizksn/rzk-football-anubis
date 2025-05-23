from .core import scrape_format, run_scraper

def scrape_redraft(page):
    scrape_format(
        page,
        format_name="Redraft",
        scorings=["Non-PPR", "0.5 PPR", "1 PPR"],
        platforms=["Sleeper", "CBS", "Consensus"],
        scrape_superflex=True
    )

if __name__ == "__main__":
    run_scraper(scrape_redraft)