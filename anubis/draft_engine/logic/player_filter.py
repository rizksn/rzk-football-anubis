from typing import List, Dict, Any, Set

def get_drafted_names(draft_board: List[List[Any]]) -> Set[str]:
    return {
        player["name"]
        for row in draft_board
        for player in row
        if player and "name" in player
    }

def get_top_available(players: List[Dict[str, Any]], drafted_names: Set[str], top_n: int = 15) -> List[Dict[str, Any]]:
    return [p for p in players if p["name"] not in drafted_names][:top_n]

def filter_positional_needs(
    candidates: List[Dict[str, any]],
    team_roster: List[Dict[str, any]],
    league_format: str = "1QB",
    current_pick_number: int = 1
) -> List[Dict[str, any]]:
    def apply_cap(position: str, max_count: int, delay_until: int):
        players_at_pos = [p for p in team_roster if p["position"] == position]
        if len(players_at_pos) >= max_count:
            return [p for p in candidates if p["position"] != position]
        elif len(players_at_pos) >= 1 and current_pick_number < delay_until:
            return [p for p in candidates if p["position"] != position]
        return candidates

    if league_format == "1QB":
        candidates = apply_cap("QB", max_count=2, delay_until=120)
        candidates = apply_cap("TE", max_count=2, delay_until=100)  # You can adjust TE logic here

    return candidates