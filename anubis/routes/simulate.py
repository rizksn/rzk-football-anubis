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

router = APIRouter()

# Load static ADP data from local file
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'draftsharks', 'redraft', 'redraft_1qb_0.5-ppr_consensus.processed.json')

@lru_cache()
def load_adp_data():
    try:
        with open(DATA_PATH, 'r') as f:
            raw = json.load(f)
            return raw["data"]
    except Exception as e:
        print(f"❌ Failed to load ADP: {e}")
        return []

# ✅ Cache scored players once on server start
SCORED_PLAYERS = score_players(load_adp_data())

@router.post("/simulate")
async def simulate_draft_plan(request: Request) -> Dict[str, Any]:
    start_time = time.time()
    body = await request.json()
    use_ai = body.get("use_ai", False)
    league_format = body.get("leagueFormat", "1QB")  # 👈 add this if not already there

    draft_board = body.get("draftBoard", [])
    team_index = body.get("teamIndex", 11)

    try:
        # Count picks and round
        picks_made = sum(1 for row in draft_board for p in row if p)
        round_number = get_round_number(picks_made)
        current_pick_number = picks_made + 1

        print(f"\n🚨 NEW PICK | Team #{team_index} | Pick #{current_pick_number} | Round {round_number}")

        # Build candidate pool
        candidates = generate_scored_candidates(
            scored_players=SCORED_PLAYERS,
            draft_board=draft_board,
            team_index=team_index,
            top_n=8,
            league_format=league_format
        )

        # Extract team roster
        team_roster = extract_team_roster(draft_board, team_index)

        # Decide pick
        if use_ai:
            # AI logic placeholder
            ...
        else:
            pick = decide_pick_math(candidates, team_roster, round_number, draft_board)
            print("✅ Math engine selected:", pick)

            return {"result": pick}

    except Exception as e:
        print("❌ Draft simulation crashed!")
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Draft simulation failed: {str(e)}")