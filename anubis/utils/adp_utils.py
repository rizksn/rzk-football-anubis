import os
from pathlib import Path

def get_valid_adp_keys(base_path: str = "anubis/data/processed") -> set[str]:
    """
    Scans the processed/ folder recursively and returns a set of valid ADP format keys
    (e.g., dynasty_1qb_1_ppr_sleeper, redraft_1qb_0_5_ppr_consensus)
    """
    base_dir = Path(base_path)
    keys = set()

    for file_path in base_dir.glob("**/*.processed.json"):
        key = file_path.stem  # removes ".json"
        if key.endswith(".processed"):
            key = key.replace(".processed", "")
        keys.add(key)

    return keys
