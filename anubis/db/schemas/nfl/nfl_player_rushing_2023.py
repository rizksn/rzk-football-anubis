from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from anubis.db.schemas.core.players import players
from anubis.db.schemas.nfl import rushing_metadata

nfl_player_rushing_2023 = Table(
    "nfl_player_rushing_2023",
    rushing_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), primary_key=True),
    Column("search_full_name", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("team", String),
    Column("position", String),
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
