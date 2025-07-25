from sqlalchemy import Table, Column, String, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from anubis.db.schemas.core import core_metadata  

users = Table(
    "users",
    core_metadata,
    Column("user_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("firebase_uid", String, nullable=False, unique=True),
    Column("email", String, nullable=False),
    Column("display_name", String),
    Column(
        "subscription_status",
        String,
        nullable=False,
        server_default="free"
    ),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    CheckConstraint("subscription_status IN ('free', 'premium')", name="valid_subscription_status"),
)
