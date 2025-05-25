from sqlalchemy import Table, Column, String, Integer, Boolean, Date, MetaData

metadata = MetaData(schema="core")  # ✅ local, schema-bound metadata

players = Table(
    "players",
    metadata,
    Column("player_id", String, primary_key=True),
    Column("full_name", String),
    Column("search_full_name", String),
    Column("first_name", String),
    Column("last_name", String),
    Column("team", String),
    Column("position", String),
    Column("fantasy_positions", String),
    Column("depth_chart_position", String),
    Column("depth_chart_order", Integer),
    Column("college", String),
    Column("height", Integer),
    Column("weight", Integer),
    Column("age", Integer),
    Column("birth_date", Date),
    Column("years_exp", Integer),
    Column("active", Boolean),
)