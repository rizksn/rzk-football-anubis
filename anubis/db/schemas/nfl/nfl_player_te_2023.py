from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from anubis.db.schemas.core.players import players
from anubis.db.schemas.nfl import receiving_metadata  

nfl_player_te_2023 = Table(
    "nfl_player_te_2023",
    receiving_metadata,
    Column("player_id", String, ForeignKey("core.players.player_id"), primary_key=True),
    Column("search_full_name", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("team", String),
    Column("position", String),

    # RECEIVING
    Column("rec", Integer),
    Column("rec_yds", Integer),
    Column("rec_td", Integer),
    Column("rec_20_plus", Integer),
    Column("rec_40_plus", Integer),
    Column("rec_long", Integer),
    Column("rec_first", Integer),
    Column("rec_first_percent", Float),
    Column("rec_fum", Integer),
    Column("rec_yac_per_rec", Float),
    Column("rec_targets", Integer),

    # RUSHING
    Column("rush_att", Integer),
    Column("rush_yds", Integer),
    Column("rush_td", Integer),
    Column("rush_20_plus", Integer),
    Column("rush_40_plus", Integer),
    Column("rush_long", Integer),
    Column("rush_first", Integer),
    Column("rush_first_percent", Float),
    Column("rush_fum", Integer),

    # PASSING
    Column("pass_yds", Integer),
    Column("pass_yds_att", Float),
    Column("pass_att", Integer),
    Column("pass_cmp", Integer),
    Column("pass_cmp_percent", Float),
    Column("pass_td", Integer),
    Column("pass_int", Integer),
    Column("pass_rate", Float),
    Column("pass_first", Integer),
    Column("pass_first_percent", Float),
    Column("pass_20_plus", Integer),
    Column("pass_40_plus", Integer),
    Column("pass_long", Integer),
    Column("pass_sck", Integer),
    Column("pass_scky", Integer),
)
