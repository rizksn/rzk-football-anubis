from typing import List, Dict, Any, Set
from draft_engine.logic.player_filter import get_drafted_names
from anubis.draft_engine.logic.score_players import score_players

def select_top_candidates(
    all_players: List[Dict[str, Any]],
    draft_board: List[List[Any]],
    team_index: int,
    top_n: int = 8
) -> List[Dict[str, Any]]:
    """
    Returns top N players to feed into the LLM based on scoring logic.
    """
    # Step 1: Get already drafted names
    drafted_names = get_drafted_names(draft_board)

    # Step 2: Filter out drafted players
    available_players = [p for p in all_players if p["name"] not in drafted_names]

    # Step 3: Score remaining players
    scored_players = score_players(available_players)

    # (Optional) Step 4: Filter by positional logic or team needs
    # — placeholder for future improvements

    # Step 5: Sort by score
    sorted_by_score = sorted(scored_players, key=lambda p: p["final_score"], reverse=True)

    # Step 6: Return top N candidates
    return sorted_by_score[:top_n]