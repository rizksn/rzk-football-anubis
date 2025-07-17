from typing import List, Dict, Any

from anubis.draft_engine.scoring.adp_scoring import score_players
from anubis.draft_engine.filters.player_filter import filter_positional_needs
from anubis.draft_engine.utils.draft_utils import get_drafted_player_ids
from anubis.draft_engine.modifiers.early_round_overrides import apply_early_round_model
from anubis.draft_engine.modifiers.contextual import apply_contextual_modifiers
from anubis.draft_engine.strategy.decide_math import decide_pick_math
from anubis.draft_engine.utils.roster_utils import extract_team_roster


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

    # 3. Score remaining players
    scored = score_players(available_players)

    # 4. Apply early-round behavior modeling (picks 1–30)
    early_result = apply_early_round_model(
        scored_players=scored,
        current_pick_number=current_pick_number,
        league_format=league_format
    )

    override = early_result.get("override_result")
    if override:
        return override

    adjusted_players = early_result.get("scored_players", scored)

    # 5. Extract current team roster
    team_roster = extract_team_roster(draft_board, team_index)

    # 6. Filter by positional needs (e.g., QB/TE caps)
    filtered = filter_positional_needs(
        adjusted_players,
        team_roster,
        league_format,
        current_pick_number
    )

    # 7. Apply contextual penalties (e.g., QB already filled)
    adjusted = apply_contextual_modifiers(
        filtered,
        team_roster,
        league_format,
        current_pick_number
    )

    # 8. Slice top-N candidates
    top_candidates = adjusted[:top_n]

    # 9. Final pick selection
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
