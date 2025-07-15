from typing import List, Dict, Any

def apply_contextual_modifiers(
    players: List[Dict[str, Any]],
    team_roster: List[Dict[str, Any]],
    league_format: str = "1QB",
    current_pick_number: int = 1
) -> List[Dict[str, Any]]:
    """
    Modifies player scores based on team context.
    - Penalizes redundant roster positions (e.g., 2nd QB or TE in 1QB formats)
    - Adds draft timing logic (e.g., delay 2nd QB until after pick 120)
    - Can be extended for round-based position boosts/nerfs
    """

    # TODO: Future idea – dynamic penalty/boost table per position
    position_counts = {}
    for player in team_roster:
        pos = player.get("position")
        if pos:
            position_counts[pos] = position_counts.get(pos, 0) + 1

    adjusted = []
    for p in players:
        score = p.get("final_score", 0)
        penalty = 0
        pos = p.get("position")

        # 🧠 Example rules (expandable):
        if league_format == "1QB":
            if pos == "QB" and position_counts.get("QB", 0) >= 1 and current_pick_number < 120:
                penalty += 20
            if pos == "TE" and position_counts.get("TE", 0) >= 1 and current_pick_number < 100:
                penalty += 25

        p_adjusted = p.copy()
        p_adjusted["adjusted_score"] = score - penalty
        adjusted.append(p_adjusted)

    # Sort descending by adjusted score
    return sorted(adjusted, key=lambda x: x["adjusted_score"], reverse=True)
