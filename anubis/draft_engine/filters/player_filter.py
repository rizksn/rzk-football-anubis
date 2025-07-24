from typing import List, Dict, Any
from anubis.draft_engine.filters.positional_strategies import FILTER_STRATEGIES

def filter_positional_needs(
    candidates: List[Dict[str, Any]],
    team_roster: List[Dict[str, Any]],
    format_key: str,
    current_pick_number: int = 1,
) -> List[Dict[str, Any]]:
    """
    Delegates positional filtering logic based on draft type and QB settings.
    If no strategy exists for this format, return players unfiltered.
    """
    format_key = format_key.lower()
    strategy_fn = FILTER_STRATEGIES.get(format_key)

    if not strategy_fn:
        print(f"⚠️ No positional filtering strategy for format: {format_key} — skipping positional filter")
        return candidates

    return strategy_fn(candidates, team_roster, current_pick_number)
