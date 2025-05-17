def get_round_number(current_pick: int, total_teams: int = 12) -> int:
    return (current_pick // total_teams) + 1