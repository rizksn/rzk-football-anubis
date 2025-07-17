import argparse
import json
from pathlib import Path
from anubis.draft_engine.pipeline.simulate import simulate_pick
from anubis.tests.utils.loaders import load_adp_data, create_empty_draft_board
from anubis.tests.utils.logging import save_segment_results

# ========== 📥 Parse CLI Args ==========
parser = argparse.ArgumentParser(description="Simulate a pick segment across all ADP formats")
parser.add_argument("--segment", type=str, required=True, help="Pick segment range, e.g. 1-6 or 25-36")
args = parser.parse_args()

segment_start, segment_end = map(int, args.segment.split("-"))
segment_folder = f"segment_{segment_start}-{segment_end}"

# ========== 🔧 Configs ==========
FORMATS_PATH = Path(__file__).parent / "formats" / "adp_formats.json"
RESULTS_DIR = Path(__file__).parent / "results" / "segments" / segment_folder
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

with open(FORMATS_PATH) as f:
    format_list = json.load(f)

print(f"\n🚀 Simulating picks 1–{segment_end} (focus: {segment_start}–{segment_end}) across {len(format_list)} formats...")

# ========== 🚀 Main Loop ==========
for fmt in format_list:
    adp_key = fmt["adp_format_key"]
    league_format = fmt["league_format"]
    qb_setting = fmt["qb_setting"]

    try:
        all_players = load_adp_data(adp_key)
    except FileNotFoundError:
        print(f"❌ Missing ADP file for: {adp_key}")
        continue

    draft_board = create_empty_draft_board(total_teams=12, rounds=(segment_end // 12) + 1)
    adp_rank_map = {player["player_id"]: idx + 1 for idx, player in enumerate(all_players)}

    picks = []
    for pick_index in range(segment_end):  # simulate picks 0 → segment_end - 1
        pick_number = pick_index + 1
        team_index = pick_index % 12

        result = simulate_pick(
            all_players=all_players,
            draft_board=draft_board,
            team_index=team_index,
            league_format=league_format,
            top_n=8,
        )

        pick = result["result"]
        explanation = result["explanation"]
        draft_board[pick_index] = [pick]

        if pick is not None:
            player_id = pick.get("player_id")
            full_name = pick.get("full_name", "Unknown")
            adp_rank = adp_rank_map.get(player_id)

            # Enhanced override logging
            prob_rank = result.get("prob_override_rank")
            prob_weight = result.get("prob_override_weight")

            if prob_rank is not None:
                if prob_rank == "fallback":
                    print(f"[🧠 ProbOverride] Pick {pick_number} → fallback (took highest-ranked player)")
                else:
                    print(f"[🧠 ProbOverride] Pick {pick_number} → Rank {prob_rank} (prob={prob_weight})")

            if player_id is None:
                print(f"⚠️ Missing player_id in pick object: {json.dumps(pick, indent=2)}")

            deviation = adp_rank - pick_number if adp_rank is not None else None

            picks.append({
                "pick_number": pick_number,
                "team_index": team_index,
                "player": pick,
                "adp_rank": adp_rank,
                "drafted_at": pick_number,
                "deviation": deviation,
                "explanation": explanation,
                "in_focus": segment_start <= pick_number <= segment_end,
                "prob_override_rank": prob_rank,
                "prob_override_weight": prob_weight
            })
        else:
            print(f"⚠️  No player returned at pick {pick_number} in format {adp_key}")
            print("🪵 Full result object:", json.dumps(result, indent=2))

    save_segment_results(
        segment_folder=segment_folder,
        format_metadata=fmt,
        picks=picks,
        start_pick=1,
        end_pick=segment_end,
        focus_range=args.segment
    )

    print(f"✅ {adp_key} → {segment_end} picks simulated")
