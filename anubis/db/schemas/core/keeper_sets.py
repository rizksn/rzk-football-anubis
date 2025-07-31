from sqlalchemy import Table, Column, String, Integer, JSON, DateTime, func, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from anubis.db.schemas.core import core_metadata
import uuid

keeper_sets = Table(
    "keeper_sets",
    core_metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("user_id", String, ForeignKey("core.users.user_id"), nullable=False),
    Column("name", String, nullable=False),
    Column("format_key", String, nullable=False),
    Column("num_teams", Integer, nullable=False),
    Column("draft_plan", JSON, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),

    UniqueConstraint("user_id", "name", name="uq_keeper_user_name"),
)

# Index to optimize user + format key lookups for keeper set loading
Index("ix_keeper_sets_user_format", keeper_sets.c.user_id, keeper_sets.c.format_key)

__all__ = ["keeper_sets"]
