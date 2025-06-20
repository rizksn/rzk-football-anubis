import json
import os
import time
import asyncio
from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any
from functools import lru_cache

# Core Draft Engine Imports
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

# Load static ADP data from local file
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'draftsharks', 'dynasty', 'dynasty_1qb_1-ppr_sleeper.processed.json')

@lru_cache()
def load_adp_data():
    try:
        with open(DATA_PATH, 'r') as f:
            raw = json.load(f)
            return raw["data"]
    except Exception as e:
        print(f"❌ Failed to load ADP: {e}")
        return []

# Cache scored players once on server start
SCORED_PLAYERS = score_players(load_adp_data())

@router.post("/simulate")
async def simulate_draft_plan(request: Request) -> Dict[str, Any]:
    start_time = time.time()
    body = await request.json()

    use_ai = body.get("use_ai", False)
    league_format = body.get("leagueFormat", "1QB")
    draft_board = body.get("draftBoard", [])
    team_index = body.get("teamIndex", 11)

    try:
        picks_made = sum(1 for row in draft_board for p in row if p)
        round_number = get_round_number(picks_made)
        current_pick_number = picks_made + 1

        print(f"\n🚨 NEW PICK | Team #{team_index} | Pick #{current_pick_number} | Round {round_number}")
        print(f"📥 use_ai={use_ai} | league_format={league_format}")
        print(f"📋 Draft board has {picks_made} picks made.")

        # ✅ Check how many scored players exist
        print(f"📊 SCORED_PLAYERS available: {len(SCORED_PLAYERS)}")

        candidates = generate_scored_candidates(
            scored_players=SCORED_PLAYERS,
            draft_board=draft_board,
            team_index=team_index,
            top_n=8,
            league_format=league_format
        )

        print(f"🎯 Candidates returned: {len(candidates)}")
        for i, p in enumerate(candidates):
            print(f"  {i+1}. {p.get('full_name', 'Unknown')} | Score: {p['final_score']:.2f}")

        team_roster = extract_team_roster(draft_board, team_index)
        print(f"🧪 Team #{team_index} roster has {len(team_roster)} players.")

        if use_ai:
            print("🤖 AI mode not implemented yet.")
            return {"error": "AI mode not active"}
        else:
            pick, explanation = decide_pick_math(candidates, team_roster, round_number, draft_board)

            if not pick:
                print("⚠️ No valid pick returned by math engine.")
                return {
                    "error": "No valid pick found",
                    "candidates": candidates,
                }

            print(f"✅ Math engine selected: {pick.get('full_name', 'Unknown')} | Explanation: {explanation}")
            print(f"⏱️ Pick took {time.time() - start_time:.2f}s")

            return {"result": pick, "explanation": explanation}

    except Exception as e:
        print("❌ Draft simulation crashed!")
        print(f"🪵 Error type: {type(e)} | Message: {repr(e)}")
        logger.exception("Unhandled exception in /simulate")
        raise HTTPException(status_code=500, detail=f"Draft simulation failed: {str(e)}")

