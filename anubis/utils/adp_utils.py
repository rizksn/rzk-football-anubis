import re
from pathlib import Path

def normalize_adp_segment(s: str) -> str:
    """Normalizes an ADP format string like '0.5' -> '0_5'."""
    return re.sub(r'[^a-z0-9]', '_', s.lower())

def get_valid_adp_keys(base_path: str = "anubis/data/processed") -> set[str]:
    base_dir = Path(base_path)
    keys = set()

    for file_path in base_dir.glob("**/*.processed.json"):
        key = file_path.stem  # removes .json
        if key.endswith(".processed"):
            key = key.replace(".processed", "")

        # Normalize the full key string, not per-segment
        normalized_key = normalize_adp_segment(key)
        keys.add(normalized_key)

    return keys
