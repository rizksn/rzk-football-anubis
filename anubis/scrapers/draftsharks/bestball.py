from .core import scrape_format, run_scraper

def scrape_bestball(page):
    scrape_format(
        page,
        format_name="Best Ball",
        scorings=["0.5 PPR", "TE Premium"],  
        platforms=["Underdog", "FFPC"],              
        scrape_superflex=False               
    )

if __name__ == "__main__":
    run_scraper(scrape_bestball)