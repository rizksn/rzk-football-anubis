
from playwright.async_api import async_playwright
import json
import asyncio
import os

def clean_header(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("fg %", "fg_percent")
    text = text.replace("xp %", "xp_percent")
    text = text.replace("long", "fg_long")
    text = text.replace("fg blk", "fg_blocked")
    text = text.replace("1-19", "fg_1_19")
    text = text.replace("20-29", "fg_20_29")
    text = text.replace("30-39", "fg_30_39")
    text = text.replace("40-49", "fg_40_49")
    text = text.replace("50-59", "fg_50_59")
    text = text.replace("60+", "fg_60_plus")
    text = text.replace(" › a-m", "")
    text = text.replace("a-m", "")
    text = text.replace(" ", "_")
    return text

async def fetch_all_nfl_stats(stat_type: str = "rushing", year: int = 2024, output_path: str = None):
    STAT_TYPE_MAPPINGS = {
        "passing": ["name", "pass_yds", "yds_att", "att", "cmp", "cmp%", "td", "int", "rate", "1st", "1st%", "20+", "40+", "long", "sck", "scky"],
        "rushing": ["name", "rush_yds", "att", "td", "20+", "40+", "long", "rush_1st", "rush_1st%", "rush_fum"],
        "receiving": ["name", "rec", "yds", "td", "20+", "40+", "lng", "rec_1st", "1st%", "rec_fum", "rec_yac/r", "tgts"],
        "field-goals": ["name", "fgm", "fga", "fg_percent", "fg_1_19", "fg_20_29", "fg_30_39", "fg_40_49", "fg_50_59", "fg_60_plus", "fg_long", "fg_blocked"]
    }

    POSITION_ABBREV = {
        "passing": "qb",
        "rushing": "rb",
        "receiving": "wr",
        "field-goals": "fg"
    }

    abbrev = POSITION_ABBREV[stat_type]

    if stat_type not in STAT_TYPE_MAPPINGS:
        raise ValueError(f"Unsupported stat_type: {stat_type}")

    if not output_path:
        base_dir = os.path.dirname(__file__)
        output_path = os.path.join(base_dir, "..", "data", "raw", f"nfl_player_{abbrev}_{year}.json")
        output_path = os.path.abspath(output_path)

    STAT_SORT_KEYS = {
        "passing": "passingyards",
        "rushing": "rushingyards",
        "receiving": "receivingreceptions",
        "field-goals": "kickingfgmade"
    }
    sort_key = STAT_SORT_KEYS[stat_type]
    url = f"https://www.nfl.com/stats/player-stats/category/{stat_type}/{year}/REG/all/{sort_key}/desc"
    print(f"🌐 Scraping {stat_type} stats from: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=250)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector("table tbody tr", timeout=15000)
        try:
            await page.click("button:has-text('Accept All Cookies')")
        except:
            pass

        all_players = []
        current_page = 1
        headers = []

        while True:
            print(f"📄 Page {current_page}")
            if current_page == 1:
                header_elements = await page.query_selector_all("table thead tr th")
                headers = [clean_header(await h.inner_text()) for h in header_elements]
                print("🧠 Parsed headers:", headers)

            rows = await page.query_selector_all("table tbody tr")
            if not rows:
                if current_page == 1:
                    print(f"⚠️ Table loaded but no rows found for {stat_type} on page 1. Skipping.")
                    await browser.close()
                    return
                else:
                    print(f"⚠️ No rows found on page {current_page}, assuming end of data.")
                    break

            for row in rows:
                cells = await row.query_selector_all("td")
                values = [await cell.inner_text() for cell in cells]
                if len(values) < len(headers):
                    continue
                player_data = dict(zip(headers, values))
                all_players.append(player_data)

            next_button = await page.query_selector('a.nfl-o-table-pagination__next')
            if not next_button or await next_button.get_attribute("aria-disabled") == "true":
                break
            await next_button.click()
            current_page += 1
            await page.wait_for_timeout(1500)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(all_players, f, indent=2)
            print(f"✅ {stat_type.upper()} stats saved to {output_path}")

        await browser.close()

async def fetch_all_positions(year: int = 2024):
    for stat_type in ["passing", "rushing", "receiving", "field-goals"]:
        await fetch_all_nfl_stats(stat_type=stat_type, year=year)

if __name__ == "__main__":
    asyncio.run(fetch_all_positions())