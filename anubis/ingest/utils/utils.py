from pathlib import Path

def parse_metadata(filename: str) -> dict:
    """
    Extracts format, type, scoring, and platform metadata from a standardized ADP filename.
    Example: "redraft_1qb_1-ppr_sleeper.processed.json"
    """
    filename = Path(filename).stem.replace(".processed", "")  # remove both .processed and .json
    parts = filename.split("_", 1)[1].split("_")
    if len(parts) < 3:
        raise ValueError(f"Invalid filename format: {filename}")

    return {
        "format": filename.split("_", 1)[0],
        "type": parts[0].upper(),
        "scoring": parts[1].replace("-", " ").upper(),
        "platform": parts[2].capitalize()
    }

def get_json_files(folder: str) -> list[str]:
    """
    Returns a list of JSON filenames in the given folder.
    """
    return [f.name for f in Path(folder).glob("*.json")]