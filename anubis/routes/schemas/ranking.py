from pydantic import BaseModel
from typing import List

class FormatRankingPayload(BaseModel):
    adp_format_key: str
    player_ids: List[str]  # Ordered by rank (1 = first)
