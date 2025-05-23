from sqlalchemy import Table, Column, Integer, String, Float
from anubis.db.base import metadata

nfl_player_wr_2024 = Table(
    "nfl_player_wr_2024",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("rec", Integer),
    Column("yds", Integer),
    Column("td", Integer),
    Column("20+", Integer, key="twenty_plus"),
    Column("40+", Integer, key="forty_plus"),
    Column("lng", Integer, key="long"),
    Column("rec_1st", Integer),
    Column("1st%", Float, key="first_percent"),
    Column("rec_fum", Integer),
    Column("rec_yac/r", Float, key="rec_yac_per_rec"),
    Column("tgts", Integer),
)