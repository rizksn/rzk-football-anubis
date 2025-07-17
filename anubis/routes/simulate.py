import json
import time
import logging
from pathlib import Path
from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any

from anubis.draft_engine.pipeline.simulate import simulate_pick
from anubis.draft_engine.scoring.adp_scoring import score_players

logger = logging.getLogger("uvicorn.error")
router = APIRouter(prefix="/api")

SCORED_ADP_CACHE = {}

def resolve_league_format(adp_format_key: str) -> str:
    if adp_format_key.startswith("redraft_"):
        return "redraft"
    elif adp_format_key.startswith("dynasty_"):
        return "dynasty"
    elif adp_format_key.startswith("rookie_"):
        return "rookie"
    elif adp_format_key.startswith("best_ball_"):
        return "best_ball"
    else:
        raise ValueError(f"Unknown ADP format: {adp_format_key}")

def load_and_score_adp(adp_format_key: str):
    """
    Load and score ADP data for a given format key.
    Results are cached for performance.
    """
    if adp_format_key in SCORED_ADP_CACHE:
        return SCORED_ADP_CACHE[adp_format_key]

    league_format = resolve_league_format(adp_format_key)
    path = (
        Path(__file__).resolve().parent.parent
        / "data" / "processed" / "draftsharks" / league_format
        / f"{adp_format_key}.processed.json"
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
    """
    Main simulation route.
    Accepts draft context, runs full pipeline, returns next pick + reasoning.
    """
    start_time = time.time()
    body = await request.json()

    adp_format_key = body.get("adpFormatKey")
    use_ai = body.get("use_ai", False)
    league_format = body.get("leagueFormat", "1QB")
    draft_plan = body.get("draftPlan")
    team_index = body.get("teamIndex")

    # 🛡️ Validate request payload
    if not adp_format_key:
        raise HTTPException(status_code=400, detail="Missing adpFormatKey")
    if not isinstance(team_index, int):
        raise HTTPException(status_code=400, detail="Missing or invalid teamIndex")
    if not isinstance(draft_plan, list):
        raise HTTPException(status_code=400, detail="Invalid draftPlan format")

    try:
        scored_players = load_and_score_adp(adp_format_key)

        logger.info(f"\n🚨 NEW PICK | Team #{team_index} | use_ai={use_ai} | format={league_format}")
        logger.info(f"📋 Picks made: {sum(1 for p in draft_plan if p.get('draftedPlayer'))} / {len(draft_plan)}")

        if use_ai:
            raise HTTPException(status_code=501, detail="AI drafting is not yet implemented.")

        response = simulate_pick(
            all_players=scored_players,
            draft_board=draft_plan,
            team_index=team_index,
            league_format=league_format,
        )

        pick = response.get("result")
        logger.info(f"✅ Picked: {pick.get('full_name', 'Unknown')} | {response.get('explanation')}")
        logger.info(f"⏱️ Completed in {time.time() - start_time:.2f}s")

        return response

    except Exception as e:
        logger.error("❌ Draft simulation crashed!", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Draft simulation failed: {str(e)}")
