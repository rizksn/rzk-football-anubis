from typing import List, Any, Dict
from collections import defaultdict

def extract_team_roster(draft_plan: List[Dict[str, Any]], team_index: int) -> List[Dict[str, Any]]:
    return [
        pick["draftedPlayer"]
        for pick in draft_plan
        if pick.get("team_index") == team_index and pick.get("draftedPlayer")
    ]


def get_team_position_counts(draft_plan: List[Dict[str, Any]], team_index: int) -> Dict[str, int]:
    counts = defaultdict(int)
    for pick in draft_plan:
        if pick.get("team_index") == team_index and pick.get("draftedPlayer"):
            position = pick["draftedPlayer"].get("position")
            if position:
                counts[position] += 1
    return dict(counts)
