from .core import scrape_format, run_scraper

def scrape_bestball(page):
    scrape_format(
        page,
        format_name="Best Ball",
        types=["1QB"],  # Only 1QB available on Underdog and FFPC
        scorings=["0.5 PPR", "TE Premium"],
        platforms=["Underdog", "FFPC"]
    )

if __name__ == "__main__":
    run_scraper(scrape_bestball)
