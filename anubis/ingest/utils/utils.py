from pathlib import Path

def parse_metadata(filename: str) -> dict:
    stem = Path(filename).stem.replace(".processed", "")
    parts = stem.split("_")

    if len(parts) < 4:
        raise ValueError(f"Invalid filename format: {filename}")

    # First component is format (can be 'redraft', 'dynasty', etc.)
    # If format is two words like 'best_ball', keep them joined.
    if parts[0] == "best" and parts[1] == "ball":
        format_name = "best_ball"
        remaining = parts[2:]
    else:
        format_name = parts[0]
        remaining = parts[1:]

    return {
        "format": format_name,
        "type": remaining[0].lower(),
        "scoring": "_".join(remaining[1:-1]).lower(),
        "platform": remaining[-1].lower()
    }

def get_json_files(folder: str) -> list[str]:
    """
    Returns a list of JSON filenames in the given folder.
    """
    return [f.name for f in Path(folder).glob("*.json")]