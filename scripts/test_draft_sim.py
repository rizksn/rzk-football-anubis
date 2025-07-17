import json
from pathlib import Path
from anubis.draft_engine.pipeline.simulate import simulate_pick

# ========== ⚙️ CONFIG ==========
ADP_FORMAT_KEY = "dynasty_1qb_1_ppr_sleeper"
LEAGUE_FORMAT = "1QB"

# ========== 📥 LOAD INPUT DATA ==========

def load_adp_data(adp_key: str) -> list:
    path = Path(__file__).parent.parent / "anubis" / "data" / "processed" / "draftsharks" / "dynasty" / f"{adp_key}.processed.json"
    with open(path, "r") as f:
        return json.load(f)["data"]

def load_draft_plan() -> list:
    return [[None] for _ in range(12 * 2)]  # 2 rounds of empty 12-team board

# ========== 🚀 RUN TEST ==========

def main():
    print("\n🚀 Running Draft Pipeline Test")

    all_players = load_adp_data(ADP_FORMAT_KEY)
    draft_board = load_draft_plan()

    picks_made = 0  # ✅ Corrected typo

    for pick_index in range(6):
        current_pick_number = picks_made + 1
        print(f"\n🟢 Simulating Pick {current_pick_number}")

        result = simulate_pick(
            all_players=all_players,
            draft_board=draft_board,
            team_index=pick_index % 12,
            league_format=LEAGUE_FORMAT,
            top_n=8,
        )

        pick = result["result"]
        explanation = result["explanation"]

        draft_board[pick_index] = [pick]
        picks_made += 1

        print("\n✅ PICK RESULT:")
        print(json.dumps(pick, indent=2))
        print("\n🧠 EXPLANATION:")
        print(explanation)

if __name__ == "__main__":
    main()
