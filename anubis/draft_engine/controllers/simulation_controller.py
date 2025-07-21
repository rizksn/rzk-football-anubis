from anubis.draft_engine.pipeline.simulate import simulate_pick

def simulate_cpu_pick(scored_players, draft_plan, team_index, league_format):
    result = simulate_pick(
        scored_players=scored_players,
        draft_board=draft_plan,
        team_index=team_index,
        league_format=league_format
    )
    return {
        "draftPlan": result["draftPlan"],
        "pickedPlayer": result["result"],
        "explanation": result["explanation"],
    }
