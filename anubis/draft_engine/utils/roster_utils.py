from typing import List, Any

def extract_team_roster(draft_plan: List[List[Any]], team_index: int) -> List[str]:
    """
    Returns a list of the drafted players for a given team_index,
    formatted as strings like 'RB: Bijan Robinson (ATL)'.
    Used for debugging, logs, or UI previews.
    """
    roster = []

    for row in draft_plan:
        # 🛡️ Skip if the row is malformed or team_index is out of range
        if not isinstance(row, list) or team_index >= len(row):
            continue

        player = row[team_index]
        if not player:
            continue

        # 📦 Extract fields whether it's a dict or an object
        if isinstance(player, dict):
            pos = player.get("position", "UNK")
            team = player.get("team", "FA")
            name = player.get("player_id") or player.get("full_name") or "Unknown"
        else:
            pos = getattr(player, "position", "UNK")
            team = getattr(player, "team", "FA")
            name = getattr(player, "player_id", None) or getattr(player, "full_name", "Unknown")

        # 🎯 Append formatted string to roster
        roster.append(f"{pos}: {name} ({team})")

    return roster
