from playwright.async_api import async_playwright
import json

async def fetch_nfl_stats(stat_type: str = "rushing", year: int = 2024):
    url = f"https://www.nfl.com/stats/player-stats/category/{stat_type}/{year}/POST/all/{stat_type}yards/desc"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Intercept API responses
        async def handle_response(response):
            if "api/v1/stats/player" in response.url and response.status == 200:
                json_data = await response.json()
                print("📦 Intercepted API data!")
                with open("nfl_stats_api.json", "w") as f:
                    json.dump(json_data, f, indent=2)

        page.on("response", handle_response)

        await page.goto(url)
        await page.wait_for_timeout(8000)  # Give time for network/XHR to fire

        await browser.close()



    # async with async_playwright() as p:
    #     browser = await p.chromium.launch(headless=False)
    #     page = await browser.new_page()
    #     await page.goto(url)

    #     try:
    #         cookie_btn = await page.query_selector("button:has-text('Accept Cookies')")
    #         if cookie_btn:
    #             await cookie_btn.click()
    #             await page.wait_for_timeout(1000)
    #     except Exception:
    #         pass

    #     await page.wait_for_function(
    #         """() => document.querySelectorAll("table.d3-o-table--detailed tbody tr").length > 10"""
    #     )
    #     await page.wait_for_timeout(1500)

    #     page_num = 1
    #     while True:
    #         print(f"📄 Scraping page {page_num}")
    #         rows = await page.query_selector_all("table.d3-o-table--detailed tbody tr")

    #         # Grab first player's name to detect pagination change
    #         first_player_name = ""
    #         if rows:
    #             first_row_cells = await rows[0].query_selector_all("td")
    #             if first_row_cells:
    #                 first_player_name = await first_row_cells[0].inner_text()

    #         if not rows:
    #             html = await page.content()
    #             with open("debug.html", "w", encoding="utf-8") as f:
    #                 f.write(html)
    #             await page.screenshot(path=f"screenshot_page_{page_num}.png", full_page=True)
    #             print("🧪 No rows found — HTML dumped and screenshot saved")

    #         print(f"🧪 Found {len(rows)} rows on page {page_num}")

    #         for row in rows:
    #             cells = await row.query_selector_all("td")
    #             if not cells or len(cells) < 10:
    #                 continue

    #             values = [await c.inner_text() for c in cells]

    #             data.append({
    #                 "name": values[0].strip(),
    #                 "rushing_yards": values[1],
    #                 "attempts": values[2],
    #                 "touchdowns": values[3],
    #                 "runs_20_plus": values[4],
    #                 "runs_40_plus": values[5],
    #                 "longest_run": values[6],
    #                 "rush_1st_downs": values[7],
    #                 "rush_1st_down_pct": values[8],
    #                 "fumbles": values[9],
    #             })

    #             print(f"✅ Parsed {values[0]} → Yards: {values[1]}, TDs: {values[3]}")

    #         # Handle pagination
    #         # Handle pagination
    #         next_btn = await page.query_selector("a[data-tracking-label='nfl-c-next-page']")

    #         if next_btn:
    #             # Confirm it is clickable
    #             is_disabled = await next_btn.get_attribute("aria-disabled")
    #             if is_disabled == "true":
    #                 break

    #             # Save current first player's name to detect page change
    #             old_first = await page.eval_on_selector(
    #                 "table.d3-o-table--detailed tbody tr:first-child td:first-child",
    #                 "el => el.textContent.trim()"
    #             )

    #             print(f"🔁 Clicking next page (current top row: {old_first})")

    #             # Force JS-level click
    #             await page.evaluate("(el) => el.click()", next_btn)

    #             # ✅ Wait until first row changes
    #             await page.wait_for_function(
    #                 f"""
    #                 () => {{
    #                     const rows = document.querySelectorAll("table.d3-o-table--detailed tbody tr");
    #                     if (!rows.length) return false;
    #                     const firstCell = rows[0].querySelector("td");
    #                     if (!firstCell) return false;
    #                     return firstCell.textContent.trim() !== "{old_first}";
    #                 }}
    #                 """
    #             )

    #             await page.wait_for_timeout(1500)
    #             page_num += 1
    #             continue
    #         else:
    #             break

    #     await browser.close()

    # return data