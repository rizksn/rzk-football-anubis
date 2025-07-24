from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any
import time
import logging
import json

from anubis.draft_engine.pipeline.simulate import simulate_pick
from anubis.draft_engine.utils.draft_utils import apply_user_pick

logger = logging.getLogger("uvicorn.error")
router = APIRouter(prefix="/api")

@router.post("/simulate")
async def simulate_draft_plan(request: Request) -> Dict[str, Any]:
    start_time = time.time()
    body = await request.json()

    scored_players = body.get("scoredPlayers")
    draft_plan = body.get("draftPlan")
    team_index = body.get("teamIndex")
    adp_format_key = body.get("adpFormatKey", "")
    league_format = body.get("leagueFormat", "1QB")
    roster_config = body.get("roster_config", {})
    selected_player_id = body.get("selectedPlayerId")
    use_ai = body.get("use_ai", False)\

    if not isinstance(scored_players, list):
        raise HTTPException(status_code=400, detail="Missing or invalid scoredPlayers")
    if not isinstance(draft_plan, list):
        raise HTTPException(status_code=400, detail="Invalid draftPlan format")
    if not isinstance(team_index, int):
        raise HTTPException(status_code=400, detail="Missing or invalid teamIndex")

    try:
        logger.info(
            f"\n📦 NEW PICK → Team {team_index} | AI: {use_ai} | Format: {league_format.upper()} | "
            f"Picks Made: {sum(1 for p in draft_plan if p.get('draftedPlayer'))}/{len(draft_plan)}"
        )

        # 👤 User Pick
        if selected_player_id:
            updated_draft_plan = apply_user_pick(draft_plan, team_index, selected_player_id, scored_players)

            player_name = next((p["full_name"] for p in scored_players if p["player_id"] == selected_player_id), "Unknown")
            logger.info(f"✅ USER PICK → {player_name} | Team {team_index} | ID: {selected_player_id}")

            return {
                "pickedPlayer": {"player_id": selected_player_id},
                "draftPlan": updated_draft_plan,
            }

        # 🤖 CPU Pick
        logger.info("🧠 CPU PICK | Top 3 Candidates: %s", [p.get("full_name") for p in scored_players[:3]])

        if use_ai:
            raise HTTPException(status_code=501, detail="AI drafting is not yet implemented.")

        payload = {
            "scored_players": scored_players,
            "draft_plan": draft_plan,
            "team_index": team_index,
            "adp_format_key": adp_format_key,
            "league_format": league_format,
            "roster_config": roster_config, 
            "top_n": 8,
        }
        logger.info("📦 Received Roster Config:\n%s", json.dumps(roster_config, indent=2))
        result = simulate_pick(payload)

        updated_draft_plan = result["draftPlan"]
        pick = result["result"]

        logger.info(f"✅ CPU PICK → {pick.get('full_name', 'Unknown')} | Team {team_index} | Elapsed: {round(time.time() - start_time, 2)}s")

        return {
            "draftPlan": updated_draft_plan,
            "pickedPlayer": pick,
            "explanation": result.get("explanation"),
        }

    except Exception as e:
        logger.error("❌ Draft simulation crashed!", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Draft simulation failed: {str(e)}")
