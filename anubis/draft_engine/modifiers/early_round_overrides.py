import random
from typing import List, Dict, Any

HIERARCHICAL_PROB_TABLE = {
    1: [
        {"if_rank_available": 1, "override": [(1, 0.7), (2, 0.3)]},
    ],
    2: [
        {"if_rank_available": 1, "override": [(1, 0.7), (2, 0.2), (3, 0.1)]},
        {"if_rank_available": 2, "override": [(2, 0.7), (3, 0.2), (1, 0.1)]},
    ],
    3: [
        {"if_rank_available": 1, "override": [(1, 0.85), (2, 0.1), (3, 0.05)]},
        {"if_rank_available": 2, "override": [(2, 0.7), (3, 0.2), (4, 0.1)]},
        {"if_rank_available": 3, "override": [(3, 0.6), (4, 0.3), (5, 0.1)]},
    ],
    4: [
        {"if_rank_available": 1, "override": [(1, 1.0)]},  # 🔒 Hard stop for Rank 1
        {"if_rank_available": 2, "override": [(2, 0.8), (3, 0.15), (4, 0.05)]},
        {"if_rank_available": 3, "override": [(3, 0.6), (4, 0.25), (5, 0.15)]},
        {"if_rank_available": 4, "override": [(4, 0.5), (5, 0.3), (6, 0.2)]},
    ],
    5: [
        {"if_rank_available": 2, "override": [(2, 1.0)]},  # 🔒 Hard stop for Rank 2
        {"if_rank_available": 3, "override": [(3, 0.7), (4, 0.2), (5, 0.1)]},
        {"if_rank_available": 4, "override": [(4, 0.5), (5, 0.3), (6, 0.2)]},
        {"if_rank_available": 5, "override": [(5, 0.5), (6, 0.3), (7, 0.2)]},
    ],
    6: [
        {"if_rank_available": 3, "override": [(3, 1.0)]},  # 🔒 Hard stop for Rank 3
        {"if_rank_available": 4, "override": [(4, 0.6), (5, 0.25), (6, 0.15)]},
        {"if_rank_available": 5, "override": [(5, 0.5), (6, 0.3), (7, 0.2)]},
        {"if_rank_available": 6, "override": [(6, 0.4), (7, 0.35), (8, 0.25)]},
    ],
}


def apply_early_round_model(
    players: List[Dict[str, Any]],  # Unscored players with rank field
    current_pick_number: int,
    league_format: str,
    drafted_ids: set
) -> Dict[str, Any]:
    from anubis.draft_engine.modifiers.early_round_overrides import HIERARCHICAL_PROB_TABLE  # optional: import here if needed

    # ✅ Only run this model for picks 1–6
    if current_pick_number not in HIERARCHICAL_PROB_TABLE:
        return {"scored_players": players}

    override_rules = HIERARCHICAL_PROB_TABLE[current_pick_number]

    # ✅ Get all players still on the board
    available_players = [
        p for p in players
        if p["player_id"] not in drafted_ids
    ]

    # ✅ Go through conditional rules one by one
    for rule in override_rules:
        target_rank = rule["if_rank_available"]
        override_candidates = rule["override"]

        # Is the target rank still on the board?
        match = next((p for p in available_players if p.get("rank") == target_rank), None)

        if match:
            # 🎯 Run override pick from this override rule
            weighted_ranks = [rank for rank, _ in override_candidates]
            weights = [weight for _, weight in override_candidates]

            picked_rank = random.choices(weighted_ranks, weights)[0]

            # If fallback, return default players
            if picked_rank == "fallback":
                print(f"🔁 ProbOverride: Fallback triggered at pick {current_pick_number}")
                return {"scored_players": players}

            selected = next(
                (p for p in available_players if p.get("rank") == picked_rank),
                None
            )

            if selected:
                print(
                    f"[🧠 ProbOverride] Pick {current_pick_number} → Rank {picked_rank} → "
                    f"{selected['full_name']} (ID: {selected['player_id']})"
                )
                return {
                    "override_result": {
                        "result": selected,
                        "explanation": f"Overridden by early-round probability model (Rank {picked_rank})",
                    }
                }
            else:
                print(f"⚠️ Rank {picked_rank} selected but no player found — continuing")

    print(f"⚠️ ProbOverride: No conditions matched at pick {current_pick_number}, using default scored players")
    return {"scored_players": players}
