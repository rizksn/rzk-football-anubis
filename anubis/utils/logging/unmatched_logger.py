import os
import json
from pathlib import Path

def log_unmatched_player(log_path: str, player_data: dict):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    try:
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                unmatched = json.load(f)
        else:
            unmatched = []
    except Exception:
        unmatched = []

    if all(entry.get("name") != player_data.get("name") for entry in unmatched):
        unmatched.append(player_data)

        with open(log_path, "w") as f:
            json.dump(unmatched, f, indent=2)