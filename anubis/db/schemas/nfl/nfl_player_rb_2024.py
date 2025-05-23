from sqlalchemy import Table, Column, Integer, String, Float
from anubis.db.base import metadata

nfl_player_rb_2024 = Table(
    "nfl_player_rb_2024",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
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