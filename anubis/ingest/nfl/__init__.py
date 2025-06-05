from .season_passing import load_qb_data
from .season_rushing import load_rb_data
from .season_receiving import load_wr_data
from .season_kicking import load_kicker_data

async def load_all_nfl_stats():
    await load_qb_data()
    await load_rb_data()
    await load_wr_data()
    await load_kicker_data()