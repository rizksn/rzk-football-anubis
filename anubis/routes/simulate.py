from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any
import time
import logging
import json

from anubis.draft_engine.controllers.simulation_controller import simulate_cpu_pick

logger = logging.getLogger("uvicorn.error")
router = APIRouter(prefix="/api")

@router.post("/simulate")
async def simulate_draft_plan(request: Request) -> Dict[str, Any]:
    start_time = time.time()
    body = await request.json()

    scored_players = body.get("scoredPlayers")
    # 🔍 DEBUG: Log top 3 players received from frontend
    logger.info("📥 Received scoredPlayers (top 3): %s", [p.get("full_name") for p in scored_players[:3]])  

    draft_plan = body.get("draftPlan")
    team_index = body.get("teamIndex")
    use_ai = body.get("use_ai", False)
    league_format = body.get("leagueFormat", "1QB")

    if not isinstance(scored_players, list):
        raise HTTPException(status_code=400, detail="Missing or invalid scoredPlayers")
    if not isinstance(draft_plan, list):
        raise HTTPException(status_code=400, detail="Invalid draftPlan format")
    if not isinstance(team_index, int):
        raise HTTPException(status_code=400, detail="Missing or invalid teamIndex")

    try:
        logger.info(
            f"\n🚨 NEW PICK | Team #{team_index} | use_ai={use_ai} | format={league_format}\n"
            f"📋 Picks made: {sum(1 for p in draft_plan if p.get('draftedPlayer'))} / {len(draft_plan)}"
        )

        if use_ai:
            raise HTTPException(status_code=501, detail="AI drafting is not yet implemented.")

        # ✅ Simulate pick using passed-in scoredPlayers
        response = simulate_cpu_pick(
            scored_players=scored_players,
            draft_plan=draft_plan,
            team_index=team_index,
            league_format=league_format,
        )

        pick = response.get("pickedPlayer")
        updated_draft_plan = response.get("draftPlan")
        # 🔍 DEBUG: Log only if early in draft
        if sum(1 for p in updated_draft_plan if p.get("draftedPlayer")) <= 5:
            logger.info("📋 Top 5 Draft Plan Slots:\n%s", json.dumps(updated_draft_plan[:5], indent=2))

        latest_pick = next((p for p in reversed(updated_draft_plan) if p.get("draftedPlayer")), None)
        if latest_pick:
            logger.info("🆕 Latest Pick Added:\n%s", json.dumps(latest_pick, indent=2))

        if not isinstance(updated_draft_plan, list):
            raise HTTPException(status_code=500, detail="Invalid draftPlan returned from simulate_cpu_pick")

        logger.info("✅ Draft pick completed", extra={
            "picked_player": pick.get("full_name", "Unknown"),
            "team_index": team_index,
            "explanation": response.get("explanation"),
            "elapsed": round(time.time() - start_time, 2)
        })

        latest_pick = next((p for p in reversed(updated_draft_plan) if p.get("draftedPlayer")), None)
        logger.info("✅ Latest pick added to draftPlan:\n%s", json.dumps(latest_pick, indent=2))

        return response

    except Exception as e:
        logger.error("❌ Draft simulation crashed!", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Draft simulation failed: {str(e)}")
