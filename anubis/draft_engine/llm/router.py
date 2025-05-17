import os

if os.getenv("USE_REMOTE_LLM") == "True":
    from anubis.llm_clients.remote_client import anubis_decide
else:
    from anubis.llm_clients.local_client import anubis_decide