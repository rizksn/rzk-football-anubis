from typing import List, Any

def extract_team_roster(draft_board: List[List[Any]], team_index: int) -> List[str]:
    roster = []
    for round in draft_board:
        if not isinstance(round, list) or team_index >= len(round):
            continue
        player = round[team_index]
        if not player:
            continue

        pos = (
            player.get("pos", "UNK")
            if isinstance(player, dict)
            else getattr(player, "pos", "UNK")
        )
        name = (
            player.get("name", "Unknown")
            if isinstance(player, dict)
            else getattr(player, "name", "Unknown")
        )
        team = (
            player.get("team", "FA")
            if isinstance(player, dict)
            else getattr(player, "team", "FA")
        )

        roster.append(f"{pos}: {name} ({team})")
    return roster