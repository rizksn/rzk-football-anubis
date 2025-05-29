import asyncio
import os
import json
import logging
from playwright.async_api import async_playwright
from anubis.scrapers.nfl.path_utils import get_stat_output_path
from anubis.scrapers.nfl.config import STAT_TYPE_MAPPINGS, STAT_SORT_KEYS, POSITION_ABBREV
from anubis.scrapers.nfl.utils import clean_header

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG if needed
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

async def fetch_player_season_stats(stat_type: str = "rushing", year: int = 2024, output_path: str = None, headless: bool = True):
    if stat_type not in STAT_TYPE_MAPPINGS:
        raise ValueError(f"Unsupported stat_type: {stat_type}")

    abbrev = POSITION_ABBREV[stat_type]
    if not output_path:
        output_path = get_stat_output_path(stat_type=stat_type, year=year)

    sort_key = STAT_SORT_KEYS[stat_type]
    url = f"https://www.nfl.com/stats/player-stats/category/{stat_type}/{year}/REG/all/{sort_key}/desc"
    logger.info(f"🌐 Scraping {stat_type} stats from: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless, slow_mo=250)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector("table tbody tr", timeout=15000)

        try:
            await page.click("button:has-text('Accept All Cookies')")
        except Exception:
            logger.debug("No cookie banner found or failed to click.")

        all_players, current_page, headers = [], 1, []

        while True:
            logger.info(f"📄 Page {current_page}")
            if current_page == 1:
                headers = [
                    clean_header(await h.inner_text())
                    for h in await page.query_selector_all("table thead tr th")
                ]
                logger.debug(f"🧠 Parsed headers: {headers}")

            rows = await page.query_selector_all("table tbody tr")
            if not rows:
                if current_page > 1:
                    logger.warning(f"⚠️ No rows found on page {current_page}, assuming end of data.")
                else:
                    logger.warning("⚠️ Page 1 loaded but no rows found. Skipping.")
                break

            for row in rows:
                values = [await cell.inner_text() for cell in await row.query_selector_all("td")]
                if len(values) >= len(headers):
                    all_players.append(dict(zip(headers, values)))

            next_button = await page.query_selector('a.nfl-o-table-pagination__next')
            if not next_button or await next_button.get_attribute("aria-disabled") == "true":
                break

            await next_button.click()
            await page.wait_for_timeout(1500)
            current_page += 1

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(all_players, f, indent=2)
        logger.info(f"✅ {stat_type.upper()} stats saved to {output_path}")
        await browser.close()

async def fetch_all_positions(year: int = 2024, headless: bool = True):
    for stat_type in STAT_TYPE_MAPPINGS.keys():
        await fetch_player_season_stats(stat_type=stat_type, year=year, headless=headless)

if __name__ == "__main__":
    asyncio.run(fetch_all_positions())