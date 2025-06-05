from sqlalchemy import MetaData

# Canonical metadata objects for each NFL stat type
passing_metadata = MetaData(schema="nfl")
rushing_metadata = MetaData(schema="nfl")
receiving_metadata = MetaData(schema="nfl")
kicking_metadata = MetaData(schema="nfl")