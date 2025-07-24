import random
from typing import List, Dict, Any

from anubis.draft_engine.modifiers.hierarchical_prob_table import HIERARCHICAL_PROB_TABLE

def apply_early_round_model(
    players: List[Dict[str, Any]],  # Unscored players with rank field
    current_pick_number: int,
    qb_setting: str,
    drafted_ids: set
) -> Dict[str, Any]:
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
