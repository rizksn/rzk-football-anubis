import os
import json
import time
from bs4 import BeautifulSoup

def save_adp_data(players, format_, type_, scoring, platform):
    fname = f"{format_}_{type_}_{scoring}_{platform}.json".lower().replace(" ", "-")

    # Correct project root: we’re 4 levels deep under backend
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    base_dir = os.path.join(project_root, "anubis", "data", "raw", "adp", "draftsharks", format_.lower())

    path = os.path.join(base_dir, fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump({"data": players}, f, indent=2)

    print(f"\n✅ Saved {len(players)} players to {path}")

def parse_adp_html(html):
    soup = BeautifulSoup(html, "html.parser")
    players = []
    rows = soup.select("table tbody tr")
    for row in rows:
        try:
            name_tag = row.select_one("td.player-name span.name")
            position_tag = row.select_one("td.player-name span.position")
            team_tag = row.select_one("td.player-name span.team")
            adp_tag = row.select_one("td.average-draft-position span.adp-value")
            if not (name_tag and position_tag and team_tag and adp_tag):
                continue
            name = name_tag.text.strip()
            position = position_tag.text.strip()
            team = team_tag.text.strip()
            adp = adp_tag.text.strip()
            players.append({
                "id": f"{name}-{team}-{position}".lower().replace(" ", "-"),
                "name": name,
                "position": position,
                "team": team,
                "adp": adp
            })
        except:
            continue
    return players

def scroll_to_load_all(page):
    page.evaluate("""
        () => new Promise((resolve) => {
            let lastCount = 0;
            let counter = 0;
            const interval = setInterval(() => {
                window.scrollBy(0, 1000);
                const rows = document.querySelectorAll("table tbody tr").length;
                if (rows === lastCount) {
                    counter++;
                    if (counter >= 3) {
                        clearInterval(interval);
                        resolve();
                    }
                } else {
                    lastCount = rows;
                    counter = 0;
                }
            }, 500);
        })
    """)

def is_superflex(page):
    try:
        return page.eval_on_selector('input[type="checkbox"]', "el => el.checked")
    except:
        return False

def set_toggle(page, to_superflex=True):
    try:
        checkbox = page.query_selector('input[type="checkbox"]')
        if not checkbox:
            print("⚠️ Toggle switch not found — skipping toggle")
            return
        current = checkbox.is_checked()
        if current != to_superflex:
            page.click(".toggle-container")
            page.wait_for_timeout(800)
    except Exception as e:
        print(f"⚠️ Error toggling superflex: {e}")

def scrape_combination(page, format_, type_, scoring, platform):
    print(f"🔍 Scraping: {format_}, {type_}, {scoring}, {platform}")
    scroll_to_load_all(page)
    html = page.content()
    players = parse_adp_html(html)

    print(f"✅ Found {len(players)} players")

    save_adp_data(players, format_, type_, scoring, platform)

def scrape_format(page, format_name, scorings, platforms, scrape_superflex):
    tabs = page.query_selector_all(".underline-menu > span")
    for tab in tabs:
        if tab.inner_text().strip() == format_name and tab.is_visible():
            tab.click()
            break
    page.wait_for_timeout(1000)

    set_toggle(page, False)  # Start in 1QB

    scoring_labels = [el.inner_text().strip() for el in page.query_selector_all(".badge-radio-group.adp-scorings .nav-item")]
    print(f"🔍 Found scoring options: {scoring_labels}")

    for scoring in scorings:
        try:
            print(f"🟢 Attempting to select scoring: {scoring}")
            page.click(f".badge-radio-group.adp-scorings .nav-item:text('{scoring}')")
            page.wait_for_timeout(800)
        except:
            continue
        platform_elements = page.query_selector_all(".badge-radio-group.adp-sources .nav-item")
        platform_labels = [el.inner_text().strip() for el in platform_elements if el.is_visible()]
        print(f"⚙️ Detected platforms: {platform_labels}")

        for platform in platform_labels:
            try:
                print(f"🟢 Attempting to select platform: {platform}")
                page.click(f".badge-radio-group.adp-sources .nav-item:text('{platform}')")
                page.wait_for_timeout(1200)
                scrape_combination(page, format_name, "1QB", scoring, platform)
            except Exception as e:
                print(f"❌ Failed to select platform {platform}: {e}")
                continue

    if scrape_superflex:
        set_toggle(page, True)
        try:
            page.click(".badge-radio-group.adp-scorings .nav-item:text('1 PPR')")
            page.wait_for_timeout(800)
            page.click(".badge-radio-group.adp-sources .nav-item:text('Sleeper')")
            page.wait_for_timeout(1200)
            scrape_combination(page, format_name, "Superflex", "1 PPR", "Sleeper")
        except:
            print(f"⚠️ Superflex combo not found for {format_name}")

def run_scraper(scrape_fn):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.draftsharks.com/adp", timeout=60000)
        scrape_fn(page)
        browser.close()