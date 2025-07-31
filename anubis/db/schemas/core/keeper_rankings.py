from sqlalchemy import Table, Column, String, Integer, DateTime, func, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from anubis.db.schemas.core import core_metadata
import uuid

keeper_rankings = Table(
    "keeper_rankings",
    core_metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),

    Column("keeper_set_id", UUID(as_uuid=True), ForeignKey("core.keeper_sets.id"), nullable=False),
    Column("player_id", String, nullable=False),
    Column("rank", Integer, nullable=False),

    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

Index("ix_keeper_rankings_keeper_set_id", keeper_rankings.c.keeper_set_id)

__all__ = ["keeper_rankings"]
