import random
from typing import List, Dict, Any, Tuple, Union

# 🎯 Probabilistic Pick Table
PROB_TABLE: Dict[int, List[Tuple[Union[int, str], float]]] = {
    1:  [(1, 0.8),  (2, 0.2)],
    2:  [(2, 0.7),  (1, 0.1),  (3, 0.2)],
    3:  [(3, 0.6),  (2, 0.2),  (4, 0.15),  ("fallback", 0.05)],
    4:  [(4, 0.6),  (3, 0.15), (5, 0.15),  (6, 0.1)],
    5:  [(5, 0.55), (4, 0.15), (6, 0.15),  (7, 0.1),  ("fallback", 0.05)],
    6:  [(6, 0.5),  (5, 0.15), (7, 0.15),  (8, 0.15), ("fallback", 0.05)],
    7:  [(7, 0.5),  (6, 0.15), (8, 0.15),  (9, 0.15), ("fallback", 0.05)],
    8:  [(8, 0.45), (7, 0.15), (9, 0.15),  (10, 0.15), ("fallback", 0.1)],
    9:  [(9, 0.45), (8, 0.15), (10, 0.15), (11, 0.15), ("fallback", 0.1)],
    10: [(10, 0.4), (9, 0.15), (11, 0.15), (12, 0.15), (13, 0.1), ("fallback", 0.05)],
    11: [(11, 0.4), (10, 0.15), (12, 0.15), (13, 0.15), (14, 0.1), ("fallback", 0.05)],
    12: [(12, 0.4), (11, 0.15), (13, 0.15), (14, 0.15), (15, 0.1), ("fallback", 0.05)],
}


def apply_early_round_model(
    scored_players: List[Dict[str, Any]],
    current_pick_number: int,
    league_format: str,
    drafted_ids: set
) -> Dict[str, Any]:
    """
    Selects a ranked override player based on pick number and weights.

    If fallback is chosen or a valid pick cannot be made, the original scored list is returned.
    """
    if current_pick_number > 12 or current_pick_number not in PROB_TABLE:
        return {"scored_players": scored_players}

    candidates = PROB_TABLE[current_pick_number]
    pick_rank = random.choices(
        population=[rank for rank, _ in candidates],
        weights=[weight for _, weight in candidates]
    )[0]

    print(f"[🧠 ProbOverride] Pick {current_pick_number} → Rank {pick_rank}")

    if pick_rank == "fallback":
        return {"scored_players": scored_players}

    # Filter out drafted players before override logic
    sorted_scored = [
        p for p in sorted(scored_players, key=lambda p: p["final_score"], reverse=True)
        if p["player_id"] not in drafted_ids
    ]

    try:
        selected_player = sorted_scored[pick_rank - 1]
        return {
            "override_result": {
                "result": selected_player,
                "explanation": f"Overridden by early-round probability model (Rank {pick_rank})",
                "prob_override_rank": pick_rank,
                "prob_override_weight": next((w for r, w in candidates if r == pick_rank), None)
            }
        }
    except IndexError:
        print(f"⚠️ ProbOverride failed: Rank {pick_rank} not found after filtering")
        return {"scored_players": scored_players}
