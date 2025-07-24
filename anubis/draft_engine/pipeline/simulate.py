from typing import List, Dict, Any
from anubis.draft_engine.utils.draft_utils import get_drafted_player_ids
from anubis.draft_engine.utils.roster_utils import extract_team_roster, get_team_position_counts
from anubis.draft_engine.filters.player_filter import filter_positional_needs
from anubis.draft_engine.modifiers.early_round_overrides import apply_early_round_model
from anubis.draft_engine.modifiers.contextual import apply_contextual_modifiers
from anubis.draft_engine.strategy.decide_math import decide_pick_math
import json 


def simulate_pick(payload: Dict[str, Any]) -> Dict[str, Any]:
    scored_players = payload["scored_players"]
    draft_plan = payload["draft_plan"]
    team_index = payload["team_index"]

    adp_format_key = payload.get("adp_format_key", "")
    print(f"\n🧪 [DEBUG] Received adpFormatKey: '{adp_format_key}'")
    print(f"🧪 [DEBUG] Split adpFormatKey → {adp_format_key.split('_')}")   
    adp_parts = adp_format_key.split("_", 2)  
    draft_format = adp_parts[0]               
    qb_setting = adp_parts[1]                
    format_key = f"{draft_format}_{qb_setting}" 

    top_n = payload.get("top_n", 8)
    roster_config = payload.get("roster_config", {})
    drafted_ids = get_drafted_player_ids(draft_plan)
    picks_made = len(drafted_ids)
    current_pick_number = picks_made + 1

    available_players = [p for p in scored_players if p["player_id"] not in drafted_ids]

    early_result = apply_early_round_model(
        players=available_players,
        current_pick_number=current_pick_number,
        qb_setting=qb_setting,
        drafted_ids=set(drafted_ids),
    )

    pick = None
    explanation = None
    prob_override_rank = None
    prob_override_weight = None
    top_candidates = []

    # 🧩 Capture roster before making the pick
    team_roster_before = extract_team_roster(draft_plan, team_index)

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

        filtered = filter_positional_needs(
            adjusted_players, team_roster_before, format_key, current_pick_number
        )

        print(f"⚙️ Using positional filter strategy: {format_key}")

        adjusted = apply_contextual_modifiers(
            players=filtered,
            draft_plan=draft_plan,
            team_index=team_index,
            roster_config=roster_config,
            qb_setting=qb_setting,
            current_pick_number=current_pick_number,
        )

        top_candidates = adjusted[:top_n]
        NUM_TEAMS = 12
        round_number = (current_pick_number - 1) // NUM_TEAMS + 1

        pick, explanation = decide_pick_math(
            candidates=top_candidates,
            team_roster=team_roster_before,
            round_number=round_number,
            draft_plan=draft_plan,
        )
        prob_override_rank = "fallback"

    if pick is None:
        raise ValueError("❌ simulate_pick failed: no player selected. Override failed and fallback logic didn't recover.")

    clean_pick = {
        "player_id": pick["player_id"],
        "full_name": pick["full_name"],
        "position": pick["position"],
        "team": pick["team"],
    }

    for pick_slot in draft_plan:
        if not pick_slot.get("draftedPlayer"):
            pick_slot["draftedPlayer"] = clean_pick
            pick_slot["team_index"] = team_index
            break

    # 🧩 Roster and position counts after the pick
    team_roster_after = extract_team_roster(draft_plan, team_index)
    pos_counts_after = get_team_position_counts(draft_plan, team_index)

    # ✅ Logging
    print(f"\n🧩 Team {team_index} roster BEFORE pick: {[p['full_name'] for p in team_roster_before]}")
    print(f"🎯 Picked: {pick['full_name']} ({pick['position']}) | "
          f"Score: {pick.get('final_score')} | "
          f"Adjusted: {pick.get('adjusted_score')} | "
          f"Explanation: {explanation}")
    print(f"🧩 Team {team_index} roster AFTER pick: {[p['full_name'] for p in team_roster_after]}")
    print(f"📊 Position counts after pick: {pos_counts_after}")

    if top_candidates:
        print("🔍 Top Candidates:")
        for p in top_candidates:
            print(f" - {p['full_name']} ({p['position']}): "
                  f"score={p['final_score']}, "
                  f"adjusted={p['adjusted_score']}, "
                  f"context={p.get('context_note')}")

    return {
        "result": pick,
        "explanation": explanation,
        "draftPlan": draft_plan,
        "prob_override_rank": prob_override_rank,
        "prob_override_weight": prob_override_weight,
    }
