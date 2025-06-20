from typing import List, Dict, Any, Set

def get_drafted_player_ids(draft_board: List[List[Any]]) -> set[str]:
    """
    Extracts the player_ids of all drafted players from the draft board.
    """
    return {
        player["player_id"]
        for row in draft_board
        for player in row
        if player and isinstance(player, dict) and "player_id" in player
    }

def get_top_available(
    players: List[Dict[str, Any]],
    drafted_ids: Set[str],
    top_n: int = 15
) -> List[Dict[str, Any]]:
    return [p for p in players if p.get("player_id") not in drafted_ids][:top_n]

def filter_positional_needs(
    candidates: List[Dict[str, Any]],
    team_roster: List[Dict[str, Any]],
    league_format: str = "1QB",
    current_pick_number: int = 1
) -> List[Dict[str, Any]]:
    def apply_cap(position: str, max_count: int, delay_until: int) -> List[Dict[str, Any]]:
        players_at_pos = [p for p in team_roster if p.get("position") == position]

        # If team has no players yet, don’t filter
        if not team_roster:
            return candidates

        # Enforce max limit
        if len(players_at_pos) >= max_count:
            return [p for p in candidates if p.get("position") != position]

        # Delay 2nd QB/TE until later rounds
        if len(players_at_pos) >= 1 and current_pick_number < delay_until:
            return [p for p in candidates if p.get("position") != position]

        return candidates

    if not team_roster:
        return candidates  # Nothing to filter on yet

    if league_format == "1QB":
        candidates = apply_cap("QB", max_count=2, delay_until=120)
        candidates = apply_cap("TE", max_count=2, delay_until=100)

    return candidates