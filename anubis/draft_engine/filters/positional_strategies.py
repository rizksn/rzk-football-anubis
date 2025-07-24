from typing import List, Dict, Any

# === 📦 Each strategy function accepts candidates, team_roster, and pick number ===

def redraft_1qb_filter(
    candidates: List[Dict[str, Any]],
    team_roster: List[Dict[str, Any]],
    current_pick_number: int,
) -> List[Dict[str, Any]]:
    """
    Redraft 1QB strategy:
    - Max 2 QBs total, no 2nd QB before pick 120
    - Max 2 TEs total, no 2nd TE before pick 100
    """

    def apply_cap(player_pool: List[Dict[str, Any]], position: str, max_count: int, delay_until: int) -> List[Dict[str, Any]]:
        players_at_pos = [p for p in team_roster if p.get("position") == position]

        if not team_roster:
            return player_pool

        if len(players_at_pos) >= max_count:
            return [p for p in player_pool if p.get("position") != position]

        if len(players_at_pos) >= 1 and current_pick_number < delay_until:
            return [p for p in player_pool if p.get("position") != position]

        return player_pool


    filtered = candidates
    filtered = apply_cap(filtered, "QB", max_count=2, delay_until=120)
    filtered = apply_cap(filtered, "TE", max_count=2, delay_until=100)
    return filtered

# === 📦 Strategy map for format-based filtering ===

FILTER_STRATEGIES: Dict[str, Any] = {
    "redraft_1qb": redraft_1qb_filter,
    # future formats like:
    # "dynasty_1qb": dynasty_1qb_filter,
    # "redraft_superflex": redraft_superflex_filter,
}
