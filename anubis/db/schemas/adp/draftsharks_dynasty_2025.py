from sqlalchemy import Table, Column, Integer, String, Float
from anubis.db.base import metadata

draftsharks_dynasty_2025 = Table(
    "draftsharks_dynasty_2025",  
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("player_id", String, nullable=False),
    Column("name", String, nullable=False),
    Column("team", String),
    Column("position", String),
    Column("adp", Float),
    Column("scoring", String),
    Column("platform", String),
    Column("type", String),
    schema="adp" 
)