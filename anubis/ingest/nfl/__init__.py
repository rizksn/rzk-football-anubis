from .season_passing import load_passing_data
from .season_rushing import load_rushing_data
from .season_receiving import load_receiving_data
from .season_kicking import load_kicker_data

async def load_all_nfl_stats():
    await load_passing_data()
    await load_rushing_data()
    await load_receiving_data()
    await load_kicker_data()