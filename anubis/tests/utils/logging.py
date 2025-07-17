import json
from pathlib import Path

def save_segment_results(segment_folder: str, format_metadata: dict, picks: list, start_pick: int, end_pick: int, focus_range: str):
    """Save the simulation results for a single format to a JSON file."""
    out_dir = Path(__file__).parent.parent / "results" / "segments" / segment_folder
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{format_metadata['adp_format_key']}.json"
    out_path = out_dir / filename

    output = {
        "adp_format_key": format_metadata["adp_format_key"],
        "league_format": format_metadata["league_format"],
        "qb_setting": format_metadata["qb_setting"],
        "scoring": format_metadata["scoring"],
        "platform": format_metadata["platform"],
        "start_pick": start_pick,
        "end_pick": end_pick,
        "segment_focus": focus_range,
        "picks": picks
    }

    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    return out_path
