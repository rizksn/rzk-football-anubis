from typing import List, Dict, Any

def apply_user_modifiers(
    players: List[Dict[str, Any]],
    user_weights: Dict[str, float] = None
) -> List[Dict[str, Any]]:
    """
    Applies user-configurable draft style modifiers to player scores.
    - Examples: boost RBs, fade rookies, favor upside
    - These act as tiebreakers, not hard overrides
    """

    if not user_weights:
        user_weights = {}

    rb_weight = user_weights.get("rb_priority", 0.0)       # e.g., 0.10 = +10% boost
    rookie_fade = user_weights.get("fade_rookies", 0.0)    # e.g., 0.15 = -15% penalty
    upside_boost = user_weights.get("favor_upside", 0.0)   # Not implemented yet (TBD)

    adjusted = []
    for p in players:
        score = p.get("adjusted_score", p.get("final_score", 0))
        pos = p.get("position")
        is_rookie = p.get("experience", "") == "R"

        if pos == "RB":
            score *= (1 + rb_weight)

        if is_rookie:
            score *= (1 - rookie_fade)

        p_adjusted = p.copy()
        p_adjusted["user_score"] = score
        adjusted.append(p_adjusted)

    return sorted(adjusted, key=lambda x: x["user_score"], reverse=True)
