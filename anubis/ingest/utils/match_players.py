from anubis.utils.normalize.name import normalize_name_for_matching, normalize_name_for_display

def match_player_by_name(search_name: str, player_pool: list[dict]) -> dict | None:
    norm_search = normalize_name_for_matching(search_name)
    alias_mapped = normalize_name_for_matching(normalize_name_for_display(search_name))  # maps alias if needed

    for player in player_pool:
        player_name = player.get("search_full_name", "")
        norm_player_name = normalize_name_for_matching(player_name)

        if norm_player_name == norm_search or norm_player_name == alias_mapped:
            return player

    return None