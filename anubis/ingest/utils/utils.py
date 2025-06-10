# import os
# import json
# from anubis.services.player import resolve_nfl_player_id

# def parse_metadata(filename: str):
#     filename = filename.replace(".processed.json", "").replace(".json", "")
#     parts = filename.split("_", 1)[1].split("_")
#     return {
#         "format": filename.split("_", 1)[0],
#         "type": parts[0].upper(),
#         "scoring": parts[1].replace("-", " ").upper(),
#         "platform": parts[2].capitalize()
#     }

# def get_json_files(folder: str):
#     return [f for f in os.listdir(folder) if f.endswith(".json")]