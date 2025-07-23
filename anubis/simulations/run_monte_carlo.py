import json
from pathlib import Path
from anubis.draft_engine.pipeline.simulate import simulate_pick
from anubis.draft_engine.scoring.adp_scoring import score_players
from anubis.simulations.aggregators.pick_stats_aggregator import PickStatsAggregator
from anubis.simulations.reporters.save_json import save_sim_log
from anubis.tests.utils.loaders import load_adp_data
from anubis.simulations.utils.timer import Timer

CONFIG_PATH = Path(__file__).parent / "configs" / "monte_carlo_config.json"

def run_simulations():
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    num_sims = config["num_simulations"]
    segment_start = config["segment_start"]
    segment_end = config["segment_end"]
    formats = config["formats_to_include"]
    save_logs = config.get("save_logs", False)

    print(f"🎯 Running {num_sims} simulations from picks {segment_start} to {segment_end}...")

    for fmt in formats:
        print(f"\n🧪 FORMAT: {fmt}")
        all_players = load_adp_data(fmt)

        if not all_players:
            print(f"⚠️ Skipping {fmt} — no players found in processed file")
            continue  

        # 🧠 Score players silently
        scored_players = score_players(all_players, verbose=False)

        # 🧩 Infer league format
        league_format = "Superflex" if "superflex" in fmt.lower() else "1QB"
        aggregator = PickStatsAggregator()

        for sim_index in range(num_sims):
            if sim_index % 100 == 0:
                print(f"🧪 {fmt} — Completed {sim_index}/{num_sims} simulations")

            draft_plan = [{"draftedPlayer": None} for _ in range((segment_end // 12 + 1) * 12)]
            sim_log = []

            for pick_index in range(segment_end):
                team_index = pick_index % 12
                payload = {
                    "scored_players": scored_players,
                    "draft_plan": draft_plan,
                    "team_index": team_index,
                    "league_format": league_format,
                    "top_n": 8,
                }
                result = simulate_pick(payload)

                pick = result["result"]
                draft_plan[pick_index]["draftedPlayer"] = pick

                sim_log.append({
                    "pick_number": pick_index + 1,
                    "team_index": team_index,
                    "player": pick,
                    "explanation": result.get("explanation"),
                    "prob_override_rank": result.get("prob_override_rank"),
                    "prob_override_weight": result.get("prob_override_weight"),
                })

                # ✅ Aggregate only if within range
                if segment_start <= pick_index < segment_end:
                    aggregator.record_pick(
                        pick_number=pick_index + 1,
                        player_name=pick["full_name"],
                        override_rank=result.get("prob_override_rank")
                    )


            if save_logs:
                save_sim_log(fmt, sim_index, sim_log)

        # 📝 Save format summary
        output_dir = Path(__file__).parent / "output"
        aggregator.save(fmt, output_dir)

if __name__ == "__main__":
    timer = Timer()
    run_simulations()
    timer.done()
