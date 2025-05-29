from anubis.db.schemas.core.players import players 
from sqlalchemy import Table, Column, Integer, String, Float, MetaData, ForeignKey

metadata = MetaData(schema="nfl")

nfl_player_receiving_2024 = Table(
    "nfl_player_receiving_2024",
    metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), primary_key=True),
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