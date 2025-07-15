from typing import List, Dict, Any, Set

# =============================
# 🧾 BASIC DRAFTED PLAYER UTILS
# =============================

def get_drafted_player_ids(draft_board: List[List[Any]]) -> set[str]:
    """
    Extracts the player_ids of all drafted players from the draft board.
    Used to remove unavailable players from candidate pool.
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
    """
    Returns top-N undrafted players based on list order.
    Typically used for fallback UI or queue building.
    """
    return [p for p in players if p.get("player_id") not in drafted_ids][:top_n]


# =============================
# 🧠 POSITIONAL LOGIC FILTERING
# =============================

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
