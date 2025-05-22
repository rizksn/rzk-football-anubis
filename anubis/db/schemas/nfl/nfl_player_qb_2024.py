from sqlalchemy import Table, Column, Integer, String, Float
from anubis.db.schemas.base import metadata

nfl_player_qb_2024 = Table(
    "nfl_player_qb_2024",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("pass_yds", Integer),
    Column("yds_att", Float),
    Column("att", Integer),
    Column("cmp", Integer),
    Column("cmp%", Float, key="cmp_percent"),
    Column("td", Integer),
    Column("int", Integer),
    Column("rate", Float),
    Column("1st", Integer, key="first"),
    Column("1st%", Float, key="first_percent"),
    Column("20+", Integer, key="twenty_plus"),
    Column("40+", Integer, key="forty_plus"),
    Column("long", Integer),
    Column("sck", Integer),
    Column("scky", Integer),
)