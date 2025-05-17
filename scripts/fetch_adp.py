import os
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'adp-consensus-ppr.json')
URL = "https://www.draftsharks.com/adp/half-ppr/consensus/12"

def scrape_adp():
    print(f"📡 Scraping: {URL}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)

        print("📜 Scrolling to load full table...")
        page.evaluate("""
            () => {
                return new Promise((resolve) => {
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
                });
            }
        """)
        print("✅ Finished scroll")

        html = page.content()
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ Wrote debug.html")
        browser.close()

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
                print("❌ Skipping row, missing one or more required cells")
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
        except Exception as e:
            print(f"⚠️ Skipping row due to error: {e}")
            continue

    with open(DATA_PATH, 'w') as f:
        json.dump({ "data": players }, f, indent=2)

    print(f"✅ Saved {len(players)} players to {DATA_PATH}")

if __name__ == "__main__":
    scrape_adp()
