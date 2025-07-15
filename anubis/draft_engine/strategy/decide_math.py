# =============================
# 🧠 FINAL DECISION LAYER (MATH MODEL)
# =============================

"""
This layer is the final step before a pick is made.

All players have already been:
- Scored (ADP-based model)
- Adjusted (format, roster, pick context)
- Filtered (positional caps, draft constraints)

At this point, we’re selecting *from a narrowed list* of candidates
with very similar scores — this layer adds realism, flavor, and human nuance.

🔮 Future-Pluggable Heuristics (Late-Stage Logic)

✅ Weighted randomness
    - Adds variety in late rounds (already implemented)

🧱 Team stacking bias
    - Slightly prefer players from the same team (WR/QB or WR/TE pairings)

📆 Bye week diversity
    - Penalize candidates that match existing roster bye weeks too heavily

🧤 Handcuff logic
    - Boost backup RBs if you already have the starter (e.g., Ty Chandler if you have Mattison)

🧘 Roster symmetry
    - Favor balanced team shapes (e.g., avoid 4 WRs before 2 RBs)

🎭 Draft personality
    - Profiles like "Aggressive", "Safe", "Zero RB" — affects final pick bias

🔄 “Shake it up” toggle
    - Randomly reach or fade a chalk player to simulate human variance

This file should ONLY influence final pick selection — not scoring, not filtering.
"""
