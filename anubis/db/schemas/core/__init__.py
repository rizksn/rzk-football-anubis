from sqlalchemy import MetaData

# This is the ONE shared metadata object for core schema
core_metadata = MetaData(schema="core")

from .players import players  
from .user import users

__all__ = ["players", "users", "core_metadata"]