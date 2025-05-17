def build_prompt(team_roster, available_players, round_number, league_format):
    player_lines = "\n".join([
        f"{p['name']} ({p['team']} - {p['position']}) – ADP: {p['adp']} – 2024: {p.get('stats', 'N/A')}"
        for p in available_players
    ])

    roster_text = ", ".join(team_roster) if team_roster else "None"

    prompt = f"""
You are a strategic fantasy football analyst. Your job is to pick the best player for a fantasy football team in a redraft league.

This is a 2025 redraft in a {league_format}.

Team has made the following picks:
{roster_text}

It is now Round {round_number}. The following players are available:

{player_lines}

⚠️ IMPORTANT: Only choose a player from the list above. Do not pick any player who is not listed. Do not invent or hallucinate names.

Only respond with the **exact full name** of the best available player to draft. No explanation. No formatting. No extra text. No position. No team. Just the name.

Example:
Bijan Robinson

DO NOT return anything else.
"""
    return prompt.strip()