from typing import List, Dict, Any

from anubis.draft_engine.utils.draft_utils import get_drafted_player_ids
from anubis.draft_engine.utils.roster_utils import extract_team_roster
from anubis.draft_engine.filters.player_filter import filter_positional_needs
from anubis.draft_engine.modifiers.early_round_overrides import apply_early_round_model
from anubis.draft_engine.modifiers.contextual import apply_contextual_modifiers
from anubis.draft_engine.strategy.decide_math import decide_pick_math


def simulate_pick(
    scored_players: List[Dict[str, Any]],
    draft_board: List[Dict[str, Any]],
    team_index: int,
    league_format: str = "1QB",
    top_n: int = 8,
) -> Dict[str, Any]:
    drafted_ids = get_drafted_player_ids(draft_board)
    picks_made = len(drafted_ids)
    current_pick_number = picks_made + 1

    # Remove already drafted players
    available_players = [p for p in scored_players if p["player_id"] not in drafted_ids]

    # Apply early round override model
    early_result = apply_early_round_model(
        scored_players=available_players,
        current_pick_number=current_pick_number,
        league_format=league_format,
        drafted_ids=set(drafted_ids),
    )

    pick = None
    explanation = None

    override = early_result.get("override_result")
    if override:
        picked_id = override["result"]["player_id"]
        if picked_id not in drafted_ids:
            pick = override["result"]
            explanation = override["explanation"]

    if pick is None:
        adjusted_players = early_result.get("scored_players", available_players)
        team_roster = extract_team_roster(draft_board, team_index)

        filtered = filter_positional_needs(
            adjusted_players, team_roster, league_format, current_pick_number
        )

        adjusted = apply_contextual_modifiers(
            filtered, team_roster, league_format, current_pick_number
        )

        top_candidates = adjusted[:top_n]
        round_number = (current_pick_number // 12) + 1  # TODO: Support dynamic team count

        pick, explanation = decide_pick_math(
            candidates=top_candidates,
            team_roster=team_roster,
            round_number=round_number,
            draft_board=draft_board,
        )

    # Update draft board
    for pick_slot in draft_board:
        if not pick_slot.get("draftedPlayer"):
            pick_slot["draftedPlayer"] = pick
            break

    return {
        "result": pick,
        "explanation": explanation,
        "draftPlan": draft_board,
    }
