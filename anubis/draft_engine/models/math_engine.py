from typing import List, Dict, Any
import random

from anubis.draft_engine.logic.score_players import convert_adp_to_absolute
from anubis.draft_engine.logic.player_filter import get_drafted_names, filter_positional_needs

def generate_scored_candidates(
    scored_players: List[Dict[str, Any]],
    draft_board: List[List[Any]],
    team_index: int,
    top_n: int = 8,
    league_format: str = "1QB"
) -> List[Dict[str, Any]]:
    """
    Filters out already drafted players, applies positional filtering and contextual penalties,
    then returns top-N adjusted candidates.
    """

    # 1. Filter out already drafted players
    drafted_names = get_drafted_names(draft_board)
    available = [p for p in scored_players if p["name"] not in drafted_names]

    # 2. Rebuild current team roster from board
    team_roster = [p for row in draft_board for p in row if p and p.get("team_index") == team_index]

    # 3. Determine current pick number
    current_pick = sum(1 for row in draft_board for cell in row if cell) + 1

    # 4. Sort full list by raw score first
    pre_filtered = sorted(available, key=lambda p: p["final_score"], reverse=True)

    # 5. Apply positional filtering (e.g., no QB if already drafted one before pick 120)
    filtered = filter_positional_needs(pre_filtered, team_roster, league_format, current_pick)

    # 6. Apply contextual penalties (e.g., TE/QB score penalty if team already has one)
    adjusted = apply_contextual_penalty(filtered, team_roster, league_format, current_pick)

    # 7. Final cleanup: if team has QB, reduce QB flooding
    if league_format == "1QB":
        has_qb = any(p["position"] == "QB" for p in team_roster)
        qb_candidates = [p for p in adjusted if p["position"] == "QB"]
        if has_qb and len(qb_candidates) > 1:
            top_qb = qb_candidates[0]
            adjusted = [p for p in adjusted if p["position"] != "QB"]  # remove all QBs
            adjusted.insert(0, top_qb)  # re-insert best QB at top (optional)
    
    # 8. Slice top-N after penalty logic
    top_adjusted = adjusted[:top_n]

    # 9. Debug log
    print("🎯 Top candidates (after penalties):")
    for rank, p in enumerate(top_adjusted):
        expected = convert_adp_to_absolute(str(p["adp"]))
        print(f"{rank+1}. {p['name']} → ADP: {p['adp']} | Abs ADP: {expected} | Score: {p['final_score']:.2f} | Adjusted: {p['adjusted_score']:.2f}")

    return top_adjusted


def apply_contextual_penalty(
    candidates: List[Dict[str, Any]],
    team_roster: List[Dict[str, Any]],
    league_format: str,
    current_pick_number: int  # Still passed in, in case you want to use it later
) -> List[Dict[str, Any]]:
    adjusted = []
    has_qb = any(p["position"] == "QB" for p in team_roster)
    has_te = any(p["position"] == "TE" for p in team_roster)

    for p in candidates:
        score = p["final_score"]
        penalty = 0

        if league_format == "1QB":
            if has_qb and p["position"] == "QB":
                penalty += 20
            if has_te and p["position"] == "TE":
                penalty += 25

        p_adjusted = p.copy()
        p_adjusted["adjusted_score"] = score - penalty
        adjusted.append(p_adjusted)

    return sorted(adjusted, key=lambda p: p["adjusted_score"], reverse=True)


def decide_pick_math(
    candidates: List[Dict[str, Any]],
    team_roster: List[str],
    round_number: int,
    draft_board: List[List[Any]]
) -> tuple[Dict[str, Any] | None, str]:
    if not candidates:
        return None, "No candidates available."

    picks_made = sum(1 for row in draft_board for cell in row if cell)
    actual = picks_made + 1

    # 🎯 Pick logic with randomness after pick 120
    if actual >= 120 and len(candidates) >= 8:
        weights = [0.25, 0.25, 0.20, 0.10, 0.08, 0.06, 0.04, 0.02]
        pick_index = random.choices(range(8), weights=weights, k=1)[0]
        best = candidates[pick_index]
        explanation = "Weighted pick"
    else:
        best = candidates[0]
        explanation = "Highest ranked by math model."

    expected = convert_adp_to_absolute(str(best["adp"]))
    deviation = actual - expected

    print(f"🏁 Picked: {best['name']} | ADP: {best['adp']} | Abs ADP: {expected} | Pick #: {actual} | Deviation: {deviation:+d}")

    return best, explanation
