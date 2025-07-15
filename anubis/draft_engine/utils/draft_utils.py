from typing import List, Dict, Any, Set

def get_drafted_player_ids(draft_board: List[List[Any]]) -> set[str]:
    """
    Extracts the player_ids of all drafted players from the draft board.
    Used to remove unavailable players from candidate pool.
    """
    return {
        player["player_id"]
        for row in draft_board
        for player in row
        if player and isinstance(player, dict) and "player_id" in player
    }


def get_top_available(
    players: List[Dict[str, Any]],
    drafted_ids: Set[str],
    top_n: int = 15
) -> List[Dict[str, Any]]:
    """
    Returns top-N undrafted players based on list order.
    Typically used for fallback UI or queue building.
    """
    return [p for p in players if p.get("player_id") not in drafted_ids][:top_n]
