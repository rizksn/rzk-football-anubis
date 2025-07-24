from typing import List, Dict, Any
from anubis.draft_engine.utils.roster_utils import get_team_position_counts

def apply_contextual_modifiers(
    players: List[Dict[str, Any]],
    draft_plan: List[List[Any]],
    team_index: int,
    roster_config: Dict[str, Any],
    qb_setting: str = "1QB",
    current_pick_number: int = 1,
) -> List[Dict[str, Any]]:
    """
    Modifies player scores based on contextual team needs.
    - Penalizes excess at a position vs starting config
    - Adds rules for 2nd QB/TE in early rounds
    """

    position_counts = get_team_position_counts(draft_plan, team_index)
    positions = roster_config.get("positions", {})  # ✅ FIXED

    adjusted = []
    for p in players:
        score = p.get("final_score", 0)
        penalty = 0
        pos = p.get("position")

        drafted = position_counts.get(pos, 0)
        allowed = positions.get(pos, {}).get("count", 0)  # ✅ FIXED

        # 1️⃣ Generic roster-aware penalty
        if drafted >= allowed:
            penalty += 5  # 🧮 Mild penalty for being a likely bench pick

        # 2️⃣ Extra penalties for 2nd QB / TE in early rounds (if not SF)
        if qb_setting == "1QB":
            if pos == "QB" and drafted >= 1 and current_pick_number < 120:
                penalty += 20
            if pos == "TE" and drafted >= 1 and current_pick_number < 100:
                penalty += 25

        p_adjusted = p.copy()
        p_adjusted["adjusted_score"] = score - penalty
        p_adjusted["context_note"] = f"{pos}: drafted={drafted}, allowed={allowed}, penalty={penalty}"
        adjusted.append(p_adjusted)

    return sorted(adjusted, key=lambda x: x["adjusted_score"], reverse=True)
