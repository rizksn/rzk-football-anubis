from .redraft import scrape_redraft
from .dynasty import scrape_dynasty
from .rookie import scrape_rookie
from .bestball import scrape_bestball

def scrape_all_adp_combinations(page):
    scrape_redraft(page)
    scrape_dynasty(page)
    scrape_rookie(page)
    scrape_bestball(page)