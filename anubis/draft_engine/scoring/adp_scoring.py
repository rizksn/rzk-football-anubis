from typing import List, Dict, Any
from anubis.draft_engine.utils.math_utils import smoothstep, variance_by_adp, random_in_range

def score_players(
    players: List[Dict[str, Any]],
    team_size: int = 12,
    total_rounds: int = 15
) -> List[Dict[str, Any]]:
    """
    Scores players using a normalized draft capital model + dynamic variance.
    - Higher score = higher value based on expected ADP
    - Late round players are scored lower but gain more variance
    - Mid-round players get a slight variance boost to simulate "chaos zone"
    """
    total_picks = team_size * total_rounds
    scored = []

    for player in players:
        absolute_adp = player.get("rank", 9999)  
        adp_display = player.get("adp", "")

        # Base score: inverse of draft cost (higher = better)
        base_score = ((total_picks - absolute_adp) / total_picks) * 100

        # Add variance: varies by ADP using power curve + mid-round boost
        variance = variance_by_adp(absolute_adp)
        noise = random_in_range(-variance, +variance)

        # Final score is base ± noise
        final_score = base_score + noise

        scored.append({
            **player,
            "absolute_adp": absolute_adp,
            "final_score": final_score,
            "_debug": {
                "adp": adp_display,
                "absolute_adp": absolute_adp,
                "base_score": f"{base_score:.2f}",
                "variance": f"{variance:.2f}",
                "noise": f"{noise:.2f}",
                "final_score": f"{final_score:.2f}"
            }
        })

    # 📊 One-time debug: log full score table on first run
    if not getattr(score_players, "_logged_once", False):
        setattr(score_players, "_logged_once", True)
        print("\n📊 Full Player Score Log (Sorted by Final Score):")

        sorted_scored = sorted(scored, key=lambda x: x["final_score"], reverse=True)
        for rank, p in enumerate(sorted_scored):
            display_name = p.get("full_name") or p.get("player_id") or "Unknown"
            adp = p["_debug"]["adp"]
            absolute_adp = int(p.get("absolute_adp", 9999))
            scored_rank = rank + 1
            deviation = abs(absolute_adp - scored_rank)

            print(f"{scored_rank:>3}. {display_name:<25} | ADP: {adp:<5} | AbsADP: {absolute_adp:<3} | Deviation: {deviation}")

    return scored
