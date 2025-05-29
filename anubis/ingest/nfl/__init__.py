from .passing import load_qb_data
from .rushing import load_rb_data
from .receiving import load_wr_data
from .kicking import load_kicker_data

async def load_all_nfl_stats():
    await load_qb_data()
    await load_rb_data()
    await load_wr_data()
    await load_kicker_data()