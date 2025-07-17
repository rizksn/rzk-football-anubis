from typing import List, Dict, Any

from anubis.draft_engine.scoring.adp_scoring import score_players
from anubis.draft_engine.filters.player_filter import filter_positional_needs
from anubis.draft_engine.utils.draft_utils import get_drafted_player_ids
from anubis.draft_engine.modifiers.early_round_overrides import apply_early_round_model, PROB_TABLE
from anubis.draft_engine.modifiers.contextual import apply_contextual_modifiers
from anubis.draft_engine.strategy.decide_math import decide_pick_math
from anubis.draft_engine.utils.roster_utils import extract_team_roster
import random


def simulate_pick(
    all_players: List[Dict[str, Any]],
    draft_board: List[List[Any]],
    team_index: int,
    league_format: str = "1QB",
    top_n: int = 8,
) -> Dict[str, Any]:
    """
    Full pick simulation pipeline:
    Scores available players, applies filters and modifiers,
    then returns the best pick + explanation.
    """

    # 1. Get drafted IDs and current pick number
    drafted_ids = get_drafted_player_ids(draft_board)
    picks_made = len(drafted_ids)
    current_pick_number = picks_made + 1

    # 2. Remove already drafted players
    available_players = [
        p for p in all_players if p["player_id"] not in drafted_ids
    ]

    # 3. Special handling for early picks (1–6) — short-circuit full pipeline
    if current_pick_number <= 6 and current_pick_number in PROB_TABLE:
        candidates = PROB_TABLE[current_pick_number]
        pick_rank = random.choices(
            population=[rank for rank, _ in candidates],
            weights=[weight for _, weight in candidates]
        )[0]

        print(f"[🧠 ProbOverride] Pick {current_pick_number} → Rank {pick_rank}")

        if pick_rank != "fallback":
            for player in available_players:
                if player.get("rank") == pick_rank:
                    return {
                        "result": player,
                        "explanation": f"Overridden by early-round probability model (Rank {pick_rank})",
                        "prob_override_rank": pick_rank,
                        "prob_override_weight": next((w for r, w in candidates if r == pick_rank), None)
                    }

    # 4. Score remaining players
    scored = score_players(available_players)

    # 5. Apply early-round behavior modeling (picks 1–30)
    early_adjusted = apply_early_round_model(
        scored_players=scored,
        current_pick_number=current_pick_number,
        league_format=league_format
    )

    # 6. Extract current team roster
    team_roster = extract_team_roster(draft_board, team_index)

    # 7. Filter by positional needs (e.g., QB/TE caps)
    filtered = filter_positional_needs(
        early_adjusted,
        team_roster,
        league_format,
        current_pick_number
    )

    # 8. Apply contextual penalties (e.g., QB already filled)
    adjusted = apply_contextual_modifiers(
        filtered,
        team_roster,
        league_format,
        current_pick_number
    )

    # 9. Slice top-N candidates
    top_candidates = adjusted[:top_n]

    # 10. Final pick selection
    round_number = (current_pick_number // 12) + 1  # TODO: support custom team count
    pick, explanation = decide_pick_math(
        candidates=top_candidates,
        team_roster=team_roster,
        round_number=round_number,
        draft_board=draft_board,
    )

    return {
        "result": pick,
        "explanation": explanation,
    }
