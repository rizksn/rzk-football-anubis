import json
from collections import defaultdict
from pathlib import Path

class PickStatsAggregator:
    def __init__(self):
        self.stats = defaultdict(lambda: defaultdict(lambda: {"total": 0, "by_override_rank": defaultdict(int)}))

    def record_pick(self, pick_number: int, player_name: str, override_rank):
        pick_slot = str(pick_number)  # use string keys for JSON compatibility
        self.stats[pick_slot][player_name]["total"] += 1
        self.stats[pick_slot][player_name]["by_override_rank"][str(override_rank)] += 1

    def save(self, format_key: str, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"summary_{format_key}.json"

        # Convert defaultdicts to normal dicts for clean JSON
        clean_dict = {
            pick: {
                player: {
                    "total": data["total"],
                    "by_override_rank": dict(data["by_override_rank"])
                }
                for player, data in player_data.items()
            }
            for pick, player_data in self.stats.items()
        }

        with open(path, "w") as f:
            json.dump(clean_dict, f, indent=2)
