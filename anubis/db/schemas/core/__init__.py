from .players import players
from sqlalchemy import MetaData

metadata = MetaData(schema="core")
players.tometadata(metadata)

__all__ = ["players", "metadata"]