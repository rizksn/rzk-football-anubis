from .core import scrape_format, run_scraper

def scrape_dynasty(page):
    scrape_format(
        page,
        format_name="Dynasty",
        types=["1QB", "Superflex"],
        scorings=["Non-PPR", "0.5 PPR", "1 PPR"],
        platforms=["Sleeper"]
    )

if __name__ == "__main__":
    run_scraper(scrape_dynasty)
