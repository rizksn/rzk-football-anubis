from sqlalchemy import Table, Column, String, DateTime, func, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from anubis.db.schemas.core import core_metadata
import uuid

adp_format_rankings = Table(
    "adp_format_rankings",
    core_metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),

    Column("user_id", String, ForeignKey("core.users.user_id"), nullable=False),
    Column("adp_format_key", String, nullable=False),
    Column("rankings", JSONB, nullable=False),  # <-- Store entire rankings list as JSONB

    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
)

# Unique index on user and format key (only one row per user+format)
Index("uq_adp_rankings_user_format", adp_format_rankings.c.user_id, adp_format_rankings.c.adp_format_key, unique=True)

__all__ = ["adp_format_rankings"]
