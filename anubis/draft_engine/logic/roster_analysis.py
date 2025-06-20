from typing import List, Any

def extract_team_roster(draft_board: List[List[Any]], team_index: int) -> List[str]:
    roster = []

    for round in draft_board:
        if not isinstance(round, list) or team_index >= len(round):
            continue

        player = round[team_index]
        if not player:
            continue

        if isinstance(player, dict):
            pos = player.get("position", "UNK")
            team = player.get("team", "FA")
            name = player.get("player_id") or player.get("full_name") or "Unknown"
        else:
            pos = getattr(player, "position", "UNK")
            team = getattr(player, "team", "FA")
            name = getattr(player, "player_id", None) or getattr(player, "full_name", "Unknown")

        roster.append(f"{pos}: {name} ({team})")

    return roster