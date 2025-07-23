from typing import List, Dict, Any
from anubis.draft_engine.utils.draft_utils import get_drafted_player_ids
from anubis.draft_engine.utils.roster_utils import extract_team_roster
from anubis.draft_engine.filters.player_filter import filter_positional_needs
from anubis.draft_engine.modifiers.early_round_overrides import apply_early_round_model
from anubis.draft_engine.modifiers.contextual import apply_contextual_modifiers
from anubis.draft_engine.strategy.decide_math import decide_pick_math


def simulate_pick(payload: Dict[str, Any]) -> Dict[str, Any]:
    scored_players = payload["scored_players"]
    draft_plan = payload["draft_plan"]
    team_index = payload["team_index"]
    league_format = payload.get("league_format", "1QB")
    top_n = payload.get("top_n", 8)

    drafted_ids = get_drafted_player_ids(draft_plan)
    picks_made = len(drafted_ids)
    current_pick_number = picks_made + 1

    available_players = [p for p in scored_players if p["player_id"] not in drafted_ids]

    early_result = apply_early_round_model(
        players=available_players,
        current_pick_number=current_pick_number,
        league_format=league_format,
        drafted_ids=set(drafted_ids),
    )

    pick = None
    explanation = None
    prob_override_rank = None
    prob_override_weight = None

    override = early_result.get("override_result")
    if override:
        picked_id = override["result"]["player_id"]
        if picked_id not in drafted_ids:
            pick = override["result"]
            explanation = override["explanation"]
            prob_override_rank = override["result"]["rank"] 
            prob_override_weight = override.get("prob_override_weight")

    if pick is None:
        adjusted_players = early_result.get("scored_players", available_players)
        team_roster = extract_team_roster(draft_plan, team_index)

        filtered = filter_positional_needs(
            adjusted_players, team_roster, league_format, current_pick_number
        )

        adjusted = apply_contextual_modifiers(
            filtered, team_roster, league_format, current_pick_number
        )

        top_candidates = adjusted[:top_n]
        NUM_TEAMS = 12
        round_number = (current_pick_number - 1) // NUM_TEAMS + 1

        pick, explanation = decide_pick_math(
            candidates=top_candidates,
            team_roster=team_roster,
            round_number=round_number,
            draft_plan=draft_plan,
        )
        prob_override_rank = "fallback"

    # Update draft board
    for pick_slot in draft_plan:
        if not pick_slot.get("draftedPlayer"):
            pick_slot["draftedPlayer"] = pick
            break

    if pick is None:
        raise ValueError("❌ simulate_pick failed: no player selected. Override failed and fallback logic didn't recover.")

    return {
        "result": pick,
        "explanation": explanation,
        "draftPlan": draft_plan,
        "prob_override_rank": prob_override_rank,
        "prob_override_weight": prob_override_weight,
    }
