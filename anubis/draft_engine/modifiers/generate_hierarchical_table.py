# anubis_ai/generate_hierarchical_table.py

def generate_hierarchical_prob_table(
    start_pick=1,
    end_pick=24,
    hard_stop_offset=3,
    decay_weights=[0.6, 0.25, 0.15]
):
    """
    Generates a hierarchical probability override table for picks `start_pick` to `end_pick`.
    
    Each pick gets:
    - One hard stop `hard_stop_offset` ranks before its pick number
    - N probability entries using the decay_weights (e.g. [0.6, 0.25, 0.15]) that span +0, +1, +2 ranks
    
    Returns:
        dict[int, list[dict]]: Mapping of pick number to override entries
    """
    prob_table = {}

    for pick in range(start_pick, end_pick + 1):
        entry_list = []

        # 1. Add 🔒 Hard stop at (pick - hard_stop_offset)
        hard_stop_rank = pick - hard_stop_offset
        if hard_stop_rank >= 1:
            entry_list.append({
                "if_rank_available": pick - 1,
                "override": [(hard_stop_rank, 1.0)]
            })

        # 2. Add probabilistic overrides starting at current rank
        for i in range(len(decay_weights)):
            if_rank = pick + i - 1
            overrides = [(pick + j - 1, decay_weights[j]) for j in range(i + 1) if (pick + j - 1) >= 1]
            entry_list.append({
                "if_rank_available": if_rank,
                "override": overrides
            })

        prob_table[pick] = entry_list

    return prob_table


if __name__ == "__main__":
    from pprint import pprint

    table = generate_hierarchical_prob_table()
    pprint(table)

