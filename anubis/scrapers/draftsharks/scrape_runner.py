from playwright.sync_api import sync_playwright

def run_scraper(scrape_fn):
    headless = False
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=200)
        page = browser.new_page()
        page.goto("https://www.draftsharks.com/adp", timeout=60000)
        scrape_fn(page)
        browser.close()
