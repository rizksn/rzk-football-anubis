from anubis.db.schemas.core.players import players 
from sqlalchemy import Table, Column, Integer, String, Float, MetaData, ForeignKey

metadata = MetaData(schema="nfl")

nfl_player_rushing_2024 = Table(
    "nfl_player_rushing_2024",
    metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), primary_key=True),
    Column("name", String, nullable=False),
    Column("rush_yds", Integer),
    Column("att", Integer),
    Column("td", Integer),
    Column("20+", Integer, key="twenty_plus"),
    Column("40+", Integer, key="forty_plus"),
    Column("long", Integer),
    Column("rush_1st", Integer),
    Column("rush_1st%", Float, key="rush_1st_percent"),
    Column("rush_fum", Integer),
)