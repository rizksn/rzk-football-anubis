import time
from .utils import scroll_to_load_all, save_adp_data
from .html_parser import parse_adp_html

def scrape_combination(page, format_, type_, scoring, platform):
    print(f"[{time.strftime('%H:%M:%S')}] 🔍 Scraping: {format_}, {type_}, {scoring}, {platform}")
    page.wait_for_timeout(5000)
    scroll_to_load_all(page)
    page.wait_for_timeout(4000)
    html = page.content()
    players = parse_adp_html(html)

    names_seen = {}
    for p in players:
        key = (p['name'], p['team'], p['position'])
        if key in names_seen:
            print(f"🔁 Duplicate: {key} (ADP {names_seen[key]} → {p['adp']})")
        names_seen[key] = p['adp']

    print(f"✅ Found {len(players)} players")
    save_adp_data(players, format_, type_, scoring, platform)


def scrape_format(page, format_name, types, scorings, platforms):
    # Click the format tab (Redraft, Dynasty, etc.)
    tabs = page.query_selector_all(".underline-menu > span")
    for tab in tabs:
        if tab.inner_text().strip() == format_name and tab.is_visible():
            tab.click()
            break
    page.wait_for_timeout(3500)

    for type_ in types:
        try:
            is_superflex_checked = page.is_checked("#superflex")
            desired_checked = (type_ == "Superflex")

            if is_superflex_checked != desired_checked:
                print(f"🟢 Toggling TYPE to: {type_}")
                page.click("label.toggle-container")
                page.wait_for_timeout(2000)
            else:
                print(f"✅ TYPE already correct: {type_}")
        except Exception as e:
            print(f"❌ Failed to verify or toggle TYPE {type_}: {e}")
            continue

        for scoring in scorings:
            try:
                print(f"🟢 Selecting SCORING: {scoring}")
                page.click(f'.badge-radio-group.adp-scorings .nav-item:text("{scoring}")')
                page.wait_for_timeout(3000)
            except Exception as e:
                print(f"❌ Failed to select scoring {scoring}: {e}")
                continue

            try:
                platform_elements = page.query_selector_all(".badge-radio-group.adp-sources .nav-item")
                platform_labels = [el.inner_text().strip() for el in platform_elements if el.is_visible()]
            except Exception as e:
                print(f"❌ Failed to read platform options: {e}")
                continue

            for platform in platform_labels:
                try:
                    print(f"🟢 Selecting PLATFORM: {platform}")
                    page.click(f'.badge-radio-group.adp-sources .nav-item:text("{platform}")')
                    page.wait_for_timeout(4000)
                    scrape_combination(page, format_name, type_, scoring, platform)
                except Exception as e:
                    print(f"❌ Failed to select platform {platform} for {type_}: {e}")
                    continue
