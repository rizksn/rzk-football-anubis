from anubis.draft_engine.llm.router import anubis_decide
from anubis.draft_engine.logic.prompt_builder import build_prompt


def decide_pick_ai(
    candidates,
    team_roster,
    round_number,
    league_format="12-team, 0.5 PPR, 1QB, 2RB, 2WR, 1TE, 2FLEX"
) -> str:
    """
    Builds a prompt from draft context and top candidates,
    sends it to the local LLM, and returns the AI's decision.
    """
    prompt = build_prompt(team_roster, candidates, round_number, league_format)
    print("📨 Prompt to LLM:\n", prompt)

    return anubis_decide(prompt)