import json
import os
import time
from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any

from anubis.draft_engine.logic.prompt_builder import build_prompt
from anubis.draft_engine.logic.roster_analysis import extract_team_roster
from anubis.draft_engine.logic.draft_state import get_round_number
from anubis.draft_engine.logic.player_selector import select_top_candidates
from anubis.draft_engine.models.math_engine import generate_scored_candidates, decide_pick_math
from anubis.draft_engine.models.ai_engine import decide_pick_ai
from anubis.draft_engine.logic.score_players import score_players

import logging
logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/api")

SCORED_ADP_CACHE = {}

def load_and_score_adp(adp_format_key: str):
    if adp_format_key in SCORED_ADP_CACHE:
        return SCORED_ADP_CACHE[adp_format_key]

    path = os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'processed', 'draftsharks', 'dynasty',
        f"{adp_format_key}.processed.json"
    )

    try:
        with open(path, 'r') as f:
            raw = json.load(f)
            scored = score_players(raw["data"])
            SCORED_ADP_CACHE[adp_format_key] = scored
            return scored
    except Exception as e:
        logger.error(f"❌ Failed to load ADP for {adp_format_key}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load ADP for {adp_format_key}")


@router.post("/simulate")
async def simulate_draft_plan(request: Request) -> Dict[str, Any]:
    start_time = time.time()
    body = await request.json()

    adp_format_key = body.get("adpFormatKey")
    if not adp_format_key:
        raise HTTPException(status_code=400, detail="Missing adpFormatKey")

    use_ai = body.get("use_ai", False)
    league_format = body.get("leagueFormat", "1QB")
    draft_plan = body.get("draftPlan")
    team_index = body.get("teamIndex")

    if team_index is None or not isinstance(team_index, int):
        raise HTTPException(status_code=400, detail="Missing or invalid teamIndex")
    if not isinstance(draft_plan, list):
        raise HTTPException(status_code=400, detail="Invalid draftPlan format")

    try:
        scored_players = load_and_score_adp(adp_format_key)

        drafted_ids = {
            p['draftedPlayer']['player_id']
            for p in draft_plan
            if p.get('draftedPlayer') and 'player_id' in p['draftedPlayer']
        }

        available_players = [
            p for p in scored_players if p['player_id'] not in drafted_ids
        ]

        picks_made = len(drafted_ids)
        round_number = get_round_number(picks_made)
        current_pick_number = picks_made + 1

        print(f"\n🚨 NEW PICK | Team #{team_index} | Pick #{current_pick_number} | Round {round_number}")
        print(f"📅 use_ai={use_ai} | league_format={league_format} | adp_format_key={adp_format_key}")
        print(f"📋 Draft plan contains {picks_made}/{len(draft_plan)} picks")
        print(f"📊 Available player pool: {len(available_players)} / {len(scored_players)}")

        candidates = generate_scored_candidates(
            scored_players=available_players,
            draft_board=draft_plan,
            team_index=team_index,
            top_n=8,
            league_format=league_format
        )

        print(f"🎯 Top {len(candidates)} candidate(s):")
        for i, p in enumerate(candidates):
            print(f"  {i+1}. {p.get('full_name', 'Unknown')} | Score: {p['final_score']:.2f}")

        team_roster = extract_team_roster(draft_plan, team_index)
        print(f"🧪 Team #{team_index} roster size: {len(team_roster)}")

        if use_ai:
            print("🤖 AI mode not implemented yet.")
            return {"error": "AI mode not active"}

        pick, explanation = decide_pick_math(candidates, team_roster, round_number, draft_plan)

        if not pick:
            print("⚠️ No valid pick returned by math engine.")
            return {
                "error": "No valid pick found",
                "candidates": candidates,
            }

        print(f"✅ Picked: {pick.get('full_name', 'Unknown')} | {explanation}")
        print(f"⏱️ Draft simulation completed in {time.time() - start_time:.2f}s")

        return {"result": pick, "explanation": explanation}

    except Exception as e:
        print("❌ Draft simulation crashed!")
        print(f"🪍 Error: {type(e).__name__} | Message: {repr(e)}")
        logger.exception("Unhandled exception in /simulate")
        raise HTTPException(status_code=500, detail=f"Draft simulation failed: {str(e)}")
