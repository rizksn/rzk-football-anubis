from typing import Optional, Dict, List, Any
from pydantic import BaseModel

class DraftPick(BaseModel):
    pickIndex: int
    round: int
    pickInRound: int
    teamIndex: int
    draftedPlayer: Optional[Dict[str, Any]] = None  

class KeeperSetPayload(BaseModel):
    user_id: str
    name: str
    format_key: str
    num_teams: int
    draft_plan: List[DraftPick]
