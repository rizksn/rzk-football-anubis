import json
from pathlib import Path

def save_json(filename: str, data: dict):
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def save_sim_log(format_key: str, sim_index: int, log_data: list):
    sim_dir = Path(__file__).parent.parent / "sim_logs" / format_key
    sim_dir.mkdir(parents=True, exist_ok=True)
    path = sim_dir / f"{sim_index}.json"
    with open(path, "w") as f:
        json.dump(log_data, f, indent=2)
