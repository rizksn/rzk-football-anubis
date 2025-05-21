from playwright.async_api import async_playwright
import json
import asyncio

async def fetch_all_nfl_stats(stat_type: str = "rushing", year: int = 2024, output_path: str = "backend/anubis/data/player_data_test.json"):
    print("🏁 Starting stat scrape...")

    url = f"https://www.nfl.com/stats/player-stats/category/{stat_type}/{year}/REG/all/{stat_type}yards/desc"
    all_players = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=250)
        page = await browser.new_page()
        await page.goto(url)
        print(f"🌐 Loaded: {url}")

        # Accept cookies if needed
        try:
            await page.click("button:has-text('Accept All Cookies')")
            print("🍪 Accepted cookies")
        except:
            pass

        current_page = 1
        while True:
            print(f"📄 Scraping page {current_page}...")

            await page.wait_for_selector("table")  # Wait until table is ready
            rows = await page.query_selector_all("table tbody tr")

            for row in rows:
                cells = await row.query_selector_all("td")
                text_values = [await cell.inner_text() for cell in cells]
                if len(text_values) < 10:
                    continue
                player_data = {
                    "name": text_values[0],
                    "rush_yds": text_values[1],
                    "att": text_values[2],
                    "td": text_values[3],
                    "20+": text_values[4],
                    "40+": text_values[5],
                    "long": text_values[6],
                    "rush_1st": text_values[7],
                    "rush_1st%": text_values[8],
                    "rush_fum": text_values[9]
                }
                all_players.append(player_data)

            # Try to click "Next Page" using the correct selector
            next_button = await page.query_selector('a.nfl-o-table-pagination__next')
            if not next_button:
                print("❌ 'Next Page' anchor not found — exiting.")
                break

            aria_disabled = await next_button.get_attribute("aria-disabled")
            if aria_disabled == "true":
                print("⛔ Reached last page.")
                break

            await next_button.click()
            current_page += 1
            await page.wait_for_timeout(1500)

        print(f"✅ Scraped {len(all_players)} players total.")
        with open(output_path, "w") as f:
            json.dump(all_players, f, indent=2)
            print(f"💾 Data saved to {output_path}")

        await browser.close()
        print("🚪 Browser closed.")

if __name__ == "__main__":
    asyncio.run(fetch_all_nfl_stats())