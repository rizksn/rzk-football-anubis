LOGGED_ONCE = False

import math
import random
from typing import List, Dict, Any

def convert_adp_to_absolute(adp: str, team_size: int = 12) -> int:
    try:
        round_str, pick_str = adp.split('.')
        round_num = int(round_str)
        pick_num = int(pick_str)
        return (round_num - 1) * team_size + pick_num
    except Exception:
        return 9999  

# def variance_by_adp(adp_rank: int, a: float = 0.0105, b: float = 1.50) -> float:
#     base = a * (adp_rank ** b)
#     if 18 <= adp_rank <= 72:
#         return base * 1.75  
#     return base

def smoothstep(x: float, edge0: float, edge1: float) -> float:
    t = max(0, min(1, (x - edge0) / (edge1 - edge0)))
    return t * t * (3 - 2 * t)

def variance_by_adp(adp_rank: int, a: float = 0.0105, b: float = 1.40) -> float:
    base = a * (adp_rank ** b)
    mid_boost = 1 + 0.75 * smoothstep(adp_rank, 18, 72)
    return base * mid_boost

def random_in_range(min_val: float, max_val: float) -> float:
    return random.uniform(min_val, max_val)

def score_players(players: List[Dict[str, Any]], team_size: int = 12, total_rounds: int = 15) -> List[Dict[str, Any]]:
    total_picks = team_size * total_rounds
    scored = []

    for player in players:
        adp = str(player.get("adp", ""))
        absolute_adp = convert_adp_to_absolute(adp, team_size)
        base_score = ((total_picks - absolute_adp) / total_picks) * 100

        variance = variance_by_adp(absolute_adp)  
        noise = random_in_range(-variance, +variance)
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

    global LOGGED_ONCE
    if not LOGGED_ONCE:
        LOGGED_ONCE = True
        print("\n📊 Full Player Score Log (Sorted by Final Score):")

        sorted_scored = sorted(scored, key=lambda x: x["final_score"], reverse=True)
        for rank, p in enumerate(sorted_scored):
            name = p["name"]
            adp = p["_debug"]["adp"]
            absolute_adp = int(p["absolute_adp"])
            scored_rank = rank + 1  # human-readable rank
            deviation = abs(absolute_adp - scored_rank)

            print(f"{scored_rank:>3}. {name:<25} | ADP: {adp:<5} | AbsADP: {absolute_adp:<3} | Deviation: {deviation}")

    return scored