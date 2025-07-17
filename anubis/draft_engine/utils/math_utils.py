import random

def smoothstep(x: float, edge0: float, edge1: float) -> float:
    """
    Sigmoid-like smoothing function to ease in/out between two edges.
    Used to boost variance for mid-round players (adds realism).
    """
    t = max(0, min(1, (x - edge0) / (edge1 - edge0)))
    return t * t * (3 - 2 * t)


def variance_by_adp(adp_rank: int, a: float = 0.0105, b: float = 1.40) -> float:
    """
    Calculates variance using a power function (a * ADP^b),
    with a smoothed mid-round boost to simulate more chaos.
    """
    base = a * (adp_rank ** b)
    mid_boost = 1 + 0.75 * smoothstep(adp_rank, 18, 72)
    return base * mid_boost


def random_in_range(min_val: float, max_val: float) -> float:
    return random.uniform(min_val, max_val)