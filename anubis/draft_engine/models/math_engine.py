from typing import List, Dict, Any
import random

from anubis.draft_engine.logic.score_players import convert_adp_to_absolute
from anubis.draft_engine.logic.player_filter import get_drafted_player_ids, filter_positional_needs

# =============================
# 🎯 CANDIDATE GENERATION PIPELINE
# =============================

def generate_scored_candidates(
    scored_players: List[Dict[str, Any]],
    draft_board: List[List[Any]],
    team_index: int,
    top_n: int = 8,
    league_format: str = "1QB"
) -> List[Dict[str, Any]]:
    """
    Core candidate selection pipeline.
    Filters drafted players, applies format-aware positional rules, contextual penalties,
    and returns the top-N adjusted players for consideration.
    """

    # 1. Remove already drafted players
    drafted_ids = get_drafted_player_ids(draft_board)
    available = [p for p in scored_players if p["player_id"] not in drafted_ids]

    # 2. Extract the team’s current roster
    team_roster = [p for row in draft_board for p in row if p and p.get("team_index") == team_index]

    # 3. Calculate current pick number (1-indexed)
    current_pick = sum(1 for row in draft_board for cell in row if cell) + 1

    # 4. Sort available pool by base model score
    pre_filtered = sorted(available, key=lambda p: p["final_score"], reverse=True)

    # 5. Filter out players based on positional rules (e.g., QB cap before pick 120)
    filtered = filter_positional_needs(pre_filtered, team_roster, league_format, current_pick)

    # 6. Penalize redundant positions already on roster (e.g., QB, TE)
    adjusted = apply_contextual_penalty(filtered, team_roster, league_format, current_pick)

    # 7. Special handling to avoid QB/TE clustering even after penalties
    if league_format == "1QB":
        has_qb = any(p["position"] == "QB" for p in team_roster)
        qb_candidates = [p for p in adjusted if p["position"] == "QB"]
        if has_qb and len(qb_candidates) > 1:
            top_qb = qb_candidates[0]
            adjusted = [p for p in adjusted if p["position"] != "QB"]
            adjusted.insert(0, top_qb)  # keep one QB candidate

    # 8. Slice top-N final list
    top_adjusted = adjusted[:top_n]

    # 9. Debug: log final pool
    print("🎯 Top candidates (after penalties):")
    for rank, p in enumerate(top_adjusted):
        expected = convert_adp_to_absolute(str(p["adp"]))
        print(f"{rank+1}. {p.get('full_name', 'Unknown')} → ADP: {p['adp']} | Abs ADP: {expected} | Score: {p['final_score']:.2f} | Adjusted: {p['adjusted_score']:.2f}")

    return top_adjusted


# =============================
# 🛠️ CONTEXTUAL ADJUSTMENTS
# =============================

def apply_contextual_penalty(
    candidates: List[Dict[str, Any]],
    team_roster: List[Dict[str, Any]],
    league_format: str,
    current_pick_number: int
) -> List[Dict[str, Any]]:
    """
    Reduces scores for positions already filled on the roster (e.g., penalize TE/QB if already drafted).
    These penalties are applied only to the current pick evaluation.
    """
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

    # Sort descending by adjusted score
    return sorted(adjusted, key=lambda p: p["adjusted_score"], reverse=True)


# =============================
# 🧠 PICK DECISION LOGIC
# =============================

def decide_pick_math(
    candidates: List[Dict[str, Any]],
    team_roster: List[str],
    round_number: int,
    draft_board: List[List[Any]]
) -> tuple[Dict[str, Any] | None, str]:
    """
    Selects the best pick based on scoring model.
    - In early/mid rounds: chooses highest ranked player.
    - In late rounds (after pick 120): uses weighted randomness to add variety.
    """

    if not candidates:
        return None, "No candidates available."

    picks_made = sum(1 for row in draft_board for cell in row if cell)
    actual_pick_number = picks_made + 1

    # Inject randomness after pick 120 to simulate human variance
    if actual_pick_number >= 120 and len(candidates) >= 8:
        weights = [0.25, 0.25, 0.20, 0.10, 0.08, 0.06, 0.04, 0.02]
        pick_index = random.choices(range(8), weights=weights, k=1)[0]
        best = candidates[pick_index]
        explanation = "Weighted pick (late round variety)"
    else:
        best = candidates[0]
        explanation = "Highest ranked by math model."

    expected = convert_adp_to_absolute(str(best["adp"]))
    deviation = actual_pick_number - expected

    print(f"🏁 Picked: {best.get('full_name', best['player_id'])} | ADP: {best['adp']} | Abs ADP: {expected} | Pick #: {actual_pick_number} | Deviation: {deviation:+d}")

    return best, explanation
