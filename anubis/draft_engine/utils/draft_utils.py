from typing import List, Dict, Any, Set

import logging
logger = logging.getLogger("uvicorn.error")

def get_drafted_player_ids(draft_board: List[Dict[str, Any]]) -> set[str]:
    drafted_ids = {
        pick["draftedPlayer"]["player_id"]
        for pick in draft_board
        if pick.get("draftedPlayer") and "player_id" in pick["draftedPlayer"]
    }
    logger.info("🔍 Extracted Drafted Player IDs: %s", drafted_ids)
    return drafted_ids

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
