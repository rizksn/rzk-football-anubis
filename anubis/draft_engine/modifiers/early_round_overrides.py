import random
from typing import List, Dict, Any, Tuple

# 🎯 Probabilistic Pick Table: maps pick number to ranked player options with weights
PROB_TABLE: Dict[int, List[Tuple[int, float]]] = {
    1: [(1, 0.8), (2, 0.2)],
    2: [(2, 0.7), (1, 0.1), (3, 0.2)],
    3: [(1, 1.0)],  # fallback safeguard example
    4: [(4, 0.6), (5, 0.25), (6, 0.1), ("fallback", 0.05)],
    5: [(5, 0.5), (6, 0.3), (7, 0.1), ("fallback", 0.1)],
    6: [(6, 0.4), (7, 0.3), (8, 0.2), ("fallback", 0.1)],
    # Extend up to 12 or 18 if needed
}

def apply_early_round_model(
    scored_players: List[Dict[str, Any]],
    current_pick_number: int,
    league_format: str
) -> List[Dict[str, Any]]:
    if current_pick_number > 12:
        return scored_players

    if current_pick_number not in PROB_TABLE:
        return scored_players

    candidates = PROB_TABLE[current_pick_number]
    pick_rank = random.choices(
        population=[rank for rank, _ in candidates],
        weights=[weight for _, weight in candidates]
    )[0]

    print(f"[🧠 ProbOverride] Pick {current_pick_number} → Rank {pick_rank}")

    if pick_rank == "fallback":
        return scored_players

    for player in scored_players:
        if player.get("rank") == pick_rank:
            # Move selected player to top
            return [player] + [p for p in scored_players if p != player]

    return scored_players  # fallback if rank not found
