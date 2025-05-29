from typing import Optional

def normalize_name(name: str) -> str:
    return name.lower().replace(" ", "").replace(".", "")

def match_player_by_name(name: str, player_pool: list[dict]) -> Optional[str]:
    """
    Returns the matching player_id from our backend player pool,
    or None if no match is found.
    """
    norm_name = normalize_name(name)
    for player in player_pool:
        if norm_name == player.get("search_full_name"):
            return player["player_id"]
    return None