# import os
# import json
# from sqlalchemy import select, func
# from sqlalchemy.ext.asyncio import AsyncSession

# from anubis.db.schemas.core.players import players as core_players_table
# from anubis.utils.normalize.name import normalize_name_for_matching

# async def resolve_nfl_player_id(session: AsyncSession, player: dict) -> str:
#     if player["position"].upper() == "DEF":
#         return None
    
#     normalized_name = normalize_name_for_matching(player["name"])
#     team = player["team"].strip().lower()
#     position = player["position"].upper()

#     stmt = select(core_players_table.c.player_id).where(
#         func.lower(core_players_table.c.team) == team,
#         core_players_table.c.search_full_name == normalized_name
#     )

#     result = await session.execute(stmt)
#     player_id = result.scalar_one_or_none()

#     if player_id is None:
#         log_path = f"logs/unmatched_draftsharks_adp_{position.lower()}s.json"
#         os.makedirs("logs", exist_ok=True)

#         try:
#             if os.path.exists(log_path):
#                 with open(log_path, "r") as f:
#                     unmatched = json.load(f)
#             else:
#                 unmatched = []
#         except Exception:
#             unmatched = []

#         if all(
#             normalize_name_for_matching(player["name"]) != normalize_name_for_matching(entry.get("name", ""))
#             for entry in unmatched
#         ):
#             unmatched.append({
#                 "name": player["name"],
#                 "team": player["team"],
#                 "position": player["position"],
#                 "normalized_name": normalized_name
#             })
#             with open(log_path, "w") as f:
#                 json.dump(unmatched, f, indent=2)

#         raise ValueError(f"❌ Could not resolve ID for {player['name']} ({player['team']} - {position})")

#     return player_id