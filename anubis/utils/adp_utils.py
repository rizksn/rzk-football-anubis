import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def normalize_adp_segment(s: str) -> str:
    """Normalizes an ADP format string like '0.5' -> '0_5'."""
    return re.sub(r'[^a-z0-9]', '_', s.lower())


def get_valid_adp_keys(base_path: str = "anubis/data/processed") -> set[str]:
    """
    Returns a set of normalized ADP format keys found under the processed folder.
    """
    base_dir = Path(base_path)
    keys = set()

    for file_path in base_dir.glob("**/*.processed.json"):
        key = file_path.stem  # removes .json
        if key.endswith(".processed"):
            key = key.replace(".processed", "")

        normalized_key = normalize_adp_segment(key)
        keys.add(normalized_key)

    return keys


def resolve_league_format(adp_format_key: str) -> str:
    """Parses the league format (e.g., redraft, dynasty) from an ADP format key."""
    if adp_format_key.startswith("redraft_"):
        logger.debug(f"Resolved format: redraft from key {adp_format_key}")
        return "redraft"
    elif adp_format_key.startswith("dynasty_"):
        logger.debug(f"Resolved format: dynasty from key {adp_format_key}")
        return "dynasty"
    elif adp_format_key.startswith("rookie_"):
        logger.debug(f"Resolved format: rookie from key {adp_format_key}")
        return "rookie"
    elif adp_format_key.startswith("best_ball_"):
        logger.debug(f"Resolved format: best_ball from key {adp_format_key}")
        return "best_ball"
    else:
        raise ValueError(f"Unknown ADP format: {adp_format_key}")
