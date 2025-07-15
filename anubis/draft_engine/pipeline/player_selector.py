from typing import List, Dict, Any
from anubis.draft_engine.filters.player_filter import get_drafted_player_ids
from anubis.draft_engine.scoring.adp_scoring import score_players

def select_top_candidates(
    all_players: List[Dict[str, Any]],
    draft_board: List[List[Any]],
    team_index: int,
    top_n: int = 8
) -> List[Dict[str, Any]]:
    """
    Returns top-N players to feed into the LLM based on scoring logic.
    """

    # 1. Get already drafted player_ids
    drafted_ids = get_drafted_player_ids(draft_board)

    # 2. Remove players who have been drafted
    available_players = [
        p for p in all_players
        if p.get("player_id") and p["player_id"] not in drafted_ids
    ]

    # 3. Score remaining players using ADP-based model
    scored_players = score_players(available_players)

    # 4. Sort by score descending
    sorted_by_score = sorted(scored_players, key=lambda p: p["final_score"], reverse=True)

    # 5. Return top-N
    return sorted_by_score[:top_n]