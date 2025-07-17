# anubis/simulations/run_monte_carlo.py

import json
from pathlib import Path
from anubis.draft_engine.pipeline.simulate import simulate_pick
from anubis.tests.utils.loaders import load_adp_data, create_empty_draft_board
from anubis.simulations.reporters.save_json import save_sim_log
from anubis.simulations.utils.timer import Timer

CONFIG_PATH = Path(__file__).parent / "configs" / "monte_carlo_config.json"

def run_simulations():
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    num_sims = config["num_simulations"]
    segment_start = config["segment_start"]
    segment_end = config["segment_end"]
    formats = config["formats_to_include"]

    print(f"🎯 Running {num_sims} simulations from picks {segment_start} to {segment_end}...")

    for fmt in formats:
        print(f"\n🧪 FORMAT: {fmt}")
        all_players = load_adp_data(fmt)

        for sim_index in range(num_sims):
            draft_board = create_empty_draft_board(total_teams=12, rounds=(segment_end // 12) + 1)
            sim_log = []

            for pick_index in range(segment_end):
                team_index = pick_index % 12
                result = simulate_pick(
                    all_players=all_players,
                    draft_board=draft_board,
                    team_index=team_index,
                    league_format="1QB",  # TODO: make dynamic later
                    top_n=8
                )

                pick = result["result"]
                draft_board[pick_index] = [pick]
                sim_log.append({
                    "pick_number": pick_index + 1,
                    "team_index": team_index,
                    "player": pick,
                    "explanation": result.get("explanation"),
                    "prob_override_rank": result.get("prob_override_rank"),
                    "prob_override_weight": result.get("prob_override_weight")
                })

            save_sim_log(fmt, sim_index, sim_log)

if __name__ == "__main__":
    timer = Timer()
    run_simulations()
    timer.done()
