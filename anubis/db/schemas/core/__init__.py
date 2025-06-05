from sqlalchemy import MetaData

# ✅ This is the ONE shared metadata object for core schema
core_metadata = MetaData(schema="core")

from .players import players  # ✅ players will now use this shared object

__all__ = ["players", "core_metadata"]