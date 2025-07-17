from typing import List, Dict, Any, Tuple
import random


def decide_pick_math(
    candidates: List[Dict[str, Any]],
    team_roster: List[Dict[str, Any]],
    round_number: int,
    draft_board: List[List[Any]],
) -> Tuple[Dict[str, Any], str]:
    """
    Placeholder pick logic: chooses the highest-scoring candidate.
    Adds basic randomness in later rounds to simulate human variance.
    """

    if not candidates:
        return None, "No candidates available"

    # 🎲 Add minor randomness after round 6 to simulate draft variation
    if round_number >= 7 and len(candidates) >= 2:
        roll = random.random()
        if roll < 0.25:
            pick = candidates[1]
            explanation = f"Selected 2nd-best candidate for variety (roll={roll:.2f})"
            return pick, explanation
        elif roll < 0.35 and len(candidates) >= 3:
            pick = candidates[2]
            explanation = f"Selected 3rd-best candidate for variety (roll={roll:.2f})"
            return pick, explanation

    # 🥇 Default: top candidate
    pick = candidates[0]
    explanation = f"Selected top candidate by final score"

    return pick, explanation
