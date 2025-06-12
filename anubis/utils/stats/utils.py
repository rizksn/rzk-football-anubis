def pad_missing_stats(player_dict: dict, all_keys: set) -> dict:
    """
    Ensures all expected stat keys exist in the player dict.
    Missing keys are filled with 0.
    """
    for key in all_keys:
        player_dict.setdefault(key, 0)
    return player_dict

def generate_all_stat_keys(mapping: dict, *field_sets: set) -> set:
    return {mapping.get(k, k) for field_set in field_sets for k in field_set}