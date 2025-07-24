HIERARCHICAL_PROB_TABLE = {
    1: [
        {"if_rank_available": 1, "override": [(1, 0.7), (2, 0.3)]},
    ],
    2: [
        {"if_rank_available": 1, "override": [(1, 0.7), (2, 0.2), (3, 0.1)]},
        {"if_rank_available": 2, "override": [(2, 0.7), (3, 0.2), (1, 0.1)]},
    ],
    3: [
        {"if_rank_available": 1, "override": [(1, 0.85), (2, 0.1), (3, 0.05)]},
        {"if_rank_available": 2, "override": [(2, 0.7), (3, 0.2), (4, 0.1)]},
        {"if_rank_available": 3, "override": [(3, 0.6), (4, 0.3), (5, 0.1)]},
    ],
    4: [
        {"if_rank_available": 1, "override": [(1, 1.0)]},  # 🔒 Hard stop for Rank 1
        {"if_rank_available": 2, "override": [(2, 0.8), (3, 0.15), (4, 0.05)]},
        {"if_rank_available": 3, "override": [(3, 0.6), (4, 0.25), (5, 0.15)]},
        {"if_rank_available": 4, "override": [(4, 0.5), (5, 0.3), (6, 0.2)]},
    ],
    5: [
        {"if_rank_available": 2, "override": [(2, 1.0)]},  # 🔒 Hard stop for Rank 2
        {"if_rank_available": 3, "override": [(3, 0.7), (4, 0.2), (5, 0.1)]},
        {"if_rank_available": 4, "override": [(4, 0.5), (5, 0.3), (6, 0.2)]},
        {"if_rank_available": 5, "override": [(5, 0.5), (6, 0.3), (7, 0.2)]},
    ],
    6: [
        {"if_rank_available": 3, "override": [(3, 1.0)]},  # 🔒 Hard stop for Rank 3
        {"if_rank_available": 4, "override": [(4, 0.6), (5, 0.25), (6, 0.15)]},
        {"if_rank_available": 5, "override": [(5, 0.5), (6, 0.3), (7, 0.2)]},
        {"if_rank_available": 6, "override": [(6, 0.4), (7, 0.35), (8, 0.25)]},
    ],
    7: [
        {"if_rank_available": 4, "override": [(4, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 5, "override": [(5, 0.6), (6, 0.25), (7, 0.15)]},
        {"if_rank_available": 6, "override": [(6, 0.5), (7, 0.3), (8, 0.2)]},
        {"if_rank_available": 7, "override": [(7, 0.4), (8, 0.35), (9, 0.25)]},
    ],
    8: [
        {"if_rank_available": 5, "override": [(5, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 6, "override": [(6, 0.6), (7, 0.25), (8, 0.15)]},
        {"if_rank_available": 7, "override": [(7, 0.5), (8, 0.3), (9, 0.2)]},
        {"if_rank_available": 8, "override": [(8, 0.4), (9, 0.35), (10, 0.25)]},
    ],
    9: [
        {"if_rank_available": 6, "override": [(6, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 7, "override": [(7, 0.6), (8, 0.25), (9, 0.15)]},
        {"if_rank_available": 8, "override": [(8, 0.5), (9, 0.3), (10, 0.2)]},
        {"if_rank_available": 9, "override": [(9, 0.4), (10, 0.35), (11, 0.25)]},
    ],
    10: [
        {"if_rank_available": 7, "override": [(7, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 8, "override": [(8, 0.6), (9, 0.25), (10, 0.15)]},
        {"if_rank_available": 9, "override": [(9, 0.5), (10, 0.3), (11, 0.2)]},
        {"if_rank_available": 10, "override": [(10, 0.4), (11, 0.35), (12, 0.25)]},
    ],
    11: [
        {"if_rank_available": 8, "override": [(8, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 9, "override": [(9, 0.6), (10, 0.25), (11, 0.15)]},
        {"if_rank_available": 10, "override": [(10, 0.5), (11, 0.3), (12, 0.2)]},
        {"if_rank_available": 11, "override": [(11, 0.4), (12, 0.35), (13, 0.25)]},
    ],
    12: [
        # No hard stop here; end of round 1 so more spread
        {"if_rank_available": 9, "override": [(9, 0.6), (10, 0.3), (11, 0.1)]},
        {"if_rank_available": 10, "override": [(10, 0.5), (11, 0.3), (12, 0.2)]},
        {"if_rank_available": 11, "override": [(11, 0.4), (12, 0.35), (13, 0.25)]},
        {"if_rank_available": 12, "override": [(12, 0.3), (13, 0.4), (14, 0.3)]},
    ],
    13: [
        {"if_rank_available": 10, "override": [(9, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 11, "override": [(11, 0.6), (12, 0.25), (13, 0.15)]},
        {"if_rank_available": 12, "override": [(12, 0.5), (13, 0.3), (14, 0.2)]},
        {"if_rank_available": 13, "override": [(13, 0.4), (14, 0.35), (15, 0.25)]},
    ],
    14: [
        {"if_rank_available": 11, "override": [(10, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 12, "override": [(12, 0.6), (13, 0.25), (14, 0.15)]},
        {"if_rank_available": 13, "override": [(13, 0.5), (14, 0.3), (15, 0.2)]},
        {"if_rank_available": 14, "override": [(14, 0.4), (15, 0.35), (16, 0.25)]},
        {"if_rank_available": 15, "override": [(15, 0.3), (16, 0.4), (17, 0.3)]},
        {"if_rank_available": 16, "override": [(16, 0.3), (17, 0.4), (18, 0.3)]},
    ],
    15: [
        {"if_rank_available": 12, "override": [(11, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 13, "override": [(13, 0.6), (14, 0.25), (15, 0.15)]},
        {"if_rank_available": 14, "override": [(14, 0.5), (15, 0.3), (16, 0.2)]},
        {"if_rank_available": 15, "override": [(15, 0.4), (16, 0.35), (17, 0.25)]},
        {"if_rank_available": 16, "override": [(16, 0.3), (17, 0.4), (18, 0.3)]},
        {"if_rank_available": 17, "override": [(17, 0.3), (18, 0.4), (19, 0.3)]},
    ],
    16: [
        {"if_rank_available": 13, "override": [(12, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 14, "override": [(14, 0.6), (15, 0.25), (16, 0.15)]},
        {"if_rank_available": 15, "override": [(15, 0.5), (16, 0.3), (17, 0.2)]},
        {"if_rank_available": 16, "override": [(16, 0.4), (17, 0.35), (18, 0.25)]},
    ],
    17: [
        {"if_rank_available": 14, "override": [(13, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 15, "override": [(15, 0.6), (16, 0.25), (17, 0.15)]},
        {"if_rank_available": 16, "override": [(16, 0.5), (17, 0.3), (18, 0.2)]},
        {"if_rank_available": 17, "override": [(17, 0.4), (18, 0.35), (19, 0.25)]},
    ],
    18: [
        {"if_rank_available": 15, "override": [(14, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 16, "override": [(16, 0.6), (17, 0.25), (18, 0.15)]},
        {"if_rank_available": 17, "override": [(17, 0.5), (18, 0.3), (19, 0.2)]},
        {"if_rank_available": 18, "override": [(18, 0.4), (19, 0.35), (20, 0.25)]},
    ],
    19: [
        {"if_rank_available": 16, "override": [(15, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 17, "override": [(17, 0.6), (18, 0.25), (19, 0.15)]},
        {"if_rank_available": 18, "override": [(18, 0.5), (19, 0.3), (20, 0.2)]},
        {"if_rank_available": 19, "override": [(19, 0.4), (20, 0.35), (21, 0.25)]},
    ],
    20: [
        {"if_rank_available": 17, "override": [(16, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 18, "override": [(18, 0.6), (19, 0.25), (20, 0.15)]},
        {"if_rank_available": 19, "override": [(19, 0.5), (20, 0.3), (21, 0.2)]},
        {"if_rank_available": 20, "override": [(20, 0.4), (21, 0.35), (22, 0.25)]},
    ],
    21: [
        {"if_rank_available": 18, "override": [(17, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 19, "override": [(19, 0.6), (20, 0.25), (21, 0.15)]},
        {"if_rank_available": 20, "override": [(20, 0.5), (21, 0.3), (22, 0.2)]},
        {"if_rank_available": 21, "override": [(21, 0.4), (22, 0.35), (23, 0.25)]},
    ],
    22: [
        {"if_rank_available": 19, "override": [(18, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 20, "override": [(20, 0.6), (21, 0.25), (22, 0.15)]},
        {"if_rank_available": 21, "override": [(21, 0.5), (22, 0.3), (23, 0.2)]},
        {"if_rank_available": 22, "override": [(22, 0.4), (23, 0.35), (24, 0.25)]},
    ],
    23: [
        {"if_rank_available": 20, "override": [(19, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 21, "override": [(21, 0.6), (22, 0.25), (23, 0.15)]},
        {"if_rank_available": 22, "override": [(22, 0.5), (23, 0.3), (24, 0.2)]},
        {"if_rank_available": 23, "override": [(23, 0.4), (24, 0.35), (25, 0.25)]},
    ],
    24: [
        {"if_rank_available": 21, "override": [(20, 1.0)]},  # 🔒 Hard stop
        {"if_rank_available": 22, "override": [(22, 0.6), (23, 0.25), (24, 0.15)]},
        {"if_rank_available": 23, "override": [(23, 0.5), (24, 0.3), (25, 0.2)]},
        {"if_rank_available": 24, "override": [(24, 0.4), (25, 0.35), (26, 0.25)]},
    ],

}