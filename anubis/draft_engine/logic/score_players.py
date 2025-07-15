import random
from typing import List, Dict, Any

# =============================
# 📐 UTILITY FUNCTIONS
# =============================

def convert_adp_to_absolute(adp: str, team_size: int = 12) -> int:
    """
    Converts ADP string (e.g. '3.04') into an absolute pick number.
    Returns 9999 on failure to deprioritize invalid ADP values.
    """
    try:
        round_str, pick_str = adp.split('.')
        round_num = int(round_str)
        pick_num = int(pick_str)
        return (round_num - 1) * team_size + pick_num
    except Exception:
        return 9999


def smoothstep(x: float, edge0: float, edge1: float) -> float:
    """
    Sigmoid-like smoothing function to ease in/out between two edges.
    Used to boost variance for mid-round players (adds realism).
    """
    t = max(0, min(1, (x - edge0) / (edge1 - edge0)))
    return t * t * (3 - 2 * t)


def variance_by_adp(adp_rank: int, a: float = 0.0105, b: float = 1.40) -> float:
    """
    Calculates variance using a power function (a * ADP^b),
    with a smoothed mid-round boost to simulate more chaos.
    """
    base = a * (adp_rank ** b)
    mid_boost = 1 + 0.75 * smoothstep(adp_rank, 18, 72)
    return base * mid_boost


def random_in_range(min_val: float, max_val: float) -> float:
    return random.uniform(min_val, max_val)


# =============================
# 🧠 PLAYER SCORING ENGINE
# =============================

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
        adp = str(player.get("adp", ""))
        absolute_adp = convert_adp_to_absolute(adp, team_size)

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
                "adp": adp,
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
