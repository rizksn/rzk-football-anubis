# Team alias mapping grouped by NFL division (readability only, structure is flat)
TEAM_ALIASES = {
    # 🏈 NFC North
    "CHI": "CHI",
    "DET": "DET",
    "GB": "GB",
    "MIN": "MIN",

    # 🏈 NFC South
    "ATL": "ATL",
    "CAR": "CAR",
    "NO": "NO",
    "TB": "TB",

    # 🏈 NFC East
    "DAL": "DAL",
    "NYG": "NYG",
    "PHI": "PHI",
    "WAS": "WAS",
    "WSH": "WAS",  # old alias

    # 🏈 NFC West
    "ARI": "ARI",
    "LAR": "LAR",
    "SEA": "SEA",
    "SF": "SF",
    "SFO": "SF",   # fallback mislabel alias

    # 🏈 AFC North
    "BAL": "BAL",
    "CIN": "CIN",
    "CLE": "CLE",
    "PIT": "PIT",

    # 🏈 AFC South
    "HOU": "HOU",
    "IND": "IND",
    "JAX": "JAX",
    "JAC": "JAX",  # alias

    # 🏈 AFC East
    "BUF": "BUF",
    "MIA": "MIA",
    "NE": "NE",
    "NEP": "NE",   # alias
    "NYJ": "NYJ",

    # 🏈 AFC West
    "DEN": "DEN",
    "KC": "KC",
    "LAC": "LAC",
    "LV": "LV",
    "LVR": "LV",   # alias

    # Deprecated teams — just in case
    "OAK": "LV",  # Optional, for legacy data only
    "STL": "LAR", # Old Rams
    "SD": "LAC",  # Old Chargers

    "UNS": "FA",  # DraftSharks "Unsigned" → standard "FA"
}

def normalize_team(team: str) -> str:
    if not team:
        return "FA"
    team = team.strip().upper()
    return TEAM_ALIASES.get(team, team)