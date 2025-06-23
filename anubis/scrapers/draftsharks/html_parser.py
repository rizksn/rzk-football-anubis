from bs4 import BeautifulSoup

def parse_adp_html(html):
    soup = BeautifulSoup(html, "html.parser")
    players = []
    seen_keys = set()

    rows = soup.select("table tbody tr")
    for row in rows:
        try:
            name_tag = row.select_one("td.player-name span.name")
            position_tag = row.select_one("td.player-name span.position")
            team_tag = row.select_one("td.player-name span.team")
            adp_tag = row.select_one("td.average-draft-position span.adp-value")
            rank_tag = row.select_one("td.rank")

            if not (name_tag and position_tag and team_tag and adp_tag and rank_tag):
                continue

            rank_text = rank_tag.text.strip()
            if not rank_text.isdigit():
                continue

            name = name_tag.text.strip()
            position = position_tag.text.strip()
            team = team_tag.text.strip()
            adp = adp_tag.text.strip()

            key = (name.lower(), position, team, adp)
            if key in seen_keys:
                continue
            seen_keys.add(key)

            players.append({
                "rank": int(rank_text),
                "name": name,
                "position": position,
                "team": team,
                "adp": adp
            })
        except Exception as e:
            print(f"⚠️ Failed to parse row for player: {name_tag.text if name_tag else '[no name]'} → {e}")
            continue
    return players
