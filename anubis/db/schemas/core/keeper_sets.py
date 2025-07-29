from sqlalchemy import Table, Column, String, Integer, JSON, DateTime, func
from anubis.db.schemas.core import core_metadata

keeper_sets = Table(
    "keeper_sets",
    core_metadata,
    Column("id", Integer, primary_key=True, index=True, autoincrement=True),  
    Column("user_id", String, nullable=False),
    Column("name", String, nullable=False),
    Column("format_key", String, nullable=False),
    Column("num_teams", Integer, nullable=False),
    Column("draft_plan", JSON, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)

__all__ = ["keeper_sets"]
