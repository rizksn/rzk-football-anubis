import os
import json
from anubis.services.player import resolve_nfl_player_id

def parse_metadata(filename: str):
    parts = filename.replace(".json", "").split("_")
    return {
        "format": parts[0],                    
        "type": parts[1].upper(),              
        "scoring": parts[2].replace("-", " ").upper(),  
        "platform": parts[3].capitalize(),     
    }

def get_json_files(folder: str):
    return [f for f in os.listdir(folder) if f.endswith(".json")]