from typing import List, Dict, Any

def apply_early_round_model(
    scored_players: List[Dict[str, Any]],
    current_pick_number: int,
    league_format: str
) -> List[Dict[str, Any]]:
    """
    Applies early round draft behavior modeling:
    - ADP drift probability rules (e.g., 1.02 becomes 1.01 20% of the time)
    - Format-specific hard overrides
    - Nudges for realism in rounds 1–3
    """
    if current_pick_number > 30:
        return scored_players  # Skip if outside early round window

    # TODO: implement override logic here (probability shifts, format-aware bumps, etc.)
    return scored_players
