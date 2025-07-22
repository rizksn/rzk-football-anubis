from typing import List, Dict, Any, Set

import logging
logger = logging.getLogger("uvicorn.error")

def get_drafted_player_ids(draft_plan: List[Dict[str, Any]]) -> set[str]:
    drafted_ids = {
        pick["draftedPlayer"]["player_id"]
        for pick in draft_plan
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

def apply_user_pick(draft_plan: list, team_index: int, player_id: str, scored_players: list = []) -> list:
    """
    Injects the user-selected player into the draft plan for the user's team.
    Uses `scored_players` to inject full player metadata if available.

    Args:
        draft_plan (list): Current draft plan (1D list of pick slots).
        team_index (int): Index of the user's team.
        player_id (str): ID of the player selected by the user.
        scored_players (list): Optional list of players with full metadata.

    Returns:
        list: Updated draft plan with the user pick injected.
    """
    # Find full player metadata (fallback if not found)
    selected_player = next((p for p in scored_players if p.get("player_id") == player_id), None)
    if not selected_player:
        selected_player = {
            "player_id": player_id,
            "full_name": "Unknown",  # Safe fallback for frontend display
        }

    # Inject into the first available pick slot for this team
    for pick in draft_plan:
        if pick.get("teamIndex") == team_index and pick.get("draftedPlayer") is None:
            pick["draftedPlayer"] = selected_player
            break

    return draft_plan
