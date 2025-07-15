from typing import List, Dict, Any

def filter_positional_needs(
    candidates: List[Dict[str, Any]],
    team_roster: List[Dict[str, Any]],
    league_format: str = "1QB",
    current_pick_number: int = 1
) -> List[Dict[str, Any]]:
    """
    Filters out players based on positional caps and draft timing rules.
    Simulates human logic: avoid overdrafting QBs/TEs early, respect roster needs.
    """

    def apply_cap(position: str, max_count: int, delay_until: int) -> List[Dict[str, Any]]:
        """
        Rules:
        - Don't allow more than `max_count` players at a position.
        - Don't take 2nd player at a position before `delay_until` pick.
        """
        players_at_pos = [p for p in team_roster if p.get("position") == position]

        # ⚠️ If team has no picks yet, don’t apply caps
        if not team_roster:
            return candidates

        # 🛑 Enforce hard max cap
        if len(players_at_pos) >= max_count:
            return [p for p in candidates if p.get("position") != position]

        # ⏳ Delay 2nd TE/QB until later in the draft
        if len(players_at_pos) >= 1 and current_pick_number < delay_until:
            return [p for p in candidates if p.get("position") != position]

        return candidates

    # 🧼 Skip filtering if roster is empty
    if not team_roster:
        return candidates

    # 📦 Apply positional filters based on league format
    if league_format == "1QB":
        # Avoid stacking QBs too early in 1QB leagues
        candidates = apply_cap("QB", max_count=2, delay_until=120)

        # Delay TE stacking to prevent early TE floods
        candidates = apply_cap("TE", max_count=2, delay_until=100)

    return candidates
