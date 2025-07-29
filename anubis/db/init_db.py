import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Core schemas
from anubis.db.schemas.core import core_metadata, players, users
from anubis.db.schemas.core.keeper_sets import keeper_sets

# NFL stat schemas
from anubis.db.schemas.nfl.nfl_player_qb_2024 import nfl_player_qb_2024
from anubis.db.schemas.nfl.nfl_player_rb_2024 import nfl_player_rb_2024
from anubis.db.schemas.nfl.nfl_player_wr_2024 import nfl_player_wr_2024
from anubis.db.schemas.nfl.nfl_player_te_2024 import nfl_player_te_2024

# Market ADP schemas (modular imports)
import anubis.db.schemas.market.draftsharks_adp_redraft as redraft_tables
import anubis.db.schemas.market.draftsharks_adp_dynasty as dynasty_tables
import anubis.db.schemas.market.draftsharks_adp_rookie as rookie_tables
import anubis.db.schemas.market.draftsharks_adp_bestball as bestball_tables

# Shared metadata
from anubis.db.schemas import (
    passing_metadata,
    rushing_metadata,
    receiving_metadata,
    kicking_metadata,
)

# Load env vars
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG_SQL = os.getenv("DEBUG_SQL", "False") == "True"

# Debug output
print("✅ core_metadata.tables:", list(core_metadata.tables.keys()))
print("✅ passing_metadata.tables:", list(passing_metadata.tables.keys()))
print("✅ players.metadata is core_metadata:", players.metadata is core_metadata)

assert "core.players" in core_metadata.tables
assert players.metadata is core_metadata

async def init():
    engine = create_async_engine(DATABASE_URL, echo=DEBUG_SQL)

    # Step 1: Ensure schemas exist
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS core"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS nfl"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS market"))

    # Step 2: Collect and create all tables
    async with engine.begin() as conn:
        def sync_create_all(sync_conn):
            all_tables = (
                list(core_metadata.tables.values())
                + list(passing_metadata.tables.values())
                + list(rushing_metadata.tables.values())
                + list(receiving_metadata.tables.values())
                + list(kicking_metadata.tables.values())
                + [
                    nfl_player_qb_2024,
                    nfl_player_rb_2024,
                    nfl_player_wr_2024,
                    nfl_player_te_2024,
                ]
                + [
                    # Redraft
                    redraft_tables.redraft_1qb_0_5_ppr_consensus,
                    redraft_tables.redraft_1qb_0_5_ppr_sleeper,
                    redraft_tables.redraft_1qb_0_5_ppr_yahoo,
                    redraft_tables.redraft_1qb_1_ppr_cbs,
                    redraft_tables.redraft_1qb_1_ppr_consensus,
                    redraft_tables.redraft_1qb_1_ppr_espn,
                    redraft_tables.redraft_1qb_1_ppr_ffpc,
                    redraft_tables.redraft_1qb_1_ppr_sleeper,
                    redraft_tables.redraft_1qb_non_ppr_cbs,
                    redraft_tables.redraft_1qb_non_ppr_consensus,
                    redraft_tables.redraft_1qb_non_ppr_sleeper,
                    redraft_tables.redraft_1qb_te_premium_ffpc, 
                    redraft_tables.redraft_superflex_1_ppr_sleeper,

                    # Dynasty
                    dynasty_tables.dynasty_1qb_non_ppr_sleeper,
                    dynasty_tables.dynasty_1qb_0_5_ppr_sleeper,
                    dynasty_tables.dynasty_1qb_1_ppr_sleeper,
                    dynasty_tables.dynasty_superflex_1_ppr_sleeper,

                    # Rookie
                    rookie_tables.rookie_1qb_1_ppr_sleeper,
                    rookie_tables.rookie_superflex_1_ppr_sleeper,

                    # Best Ball
                    bestball_tables.best_ball_1qb_0_5_ppr_underdog,
                    bestball_tables.best_ball_1qb_te_premium_ffpc,
                ]
            )
            for table in all_tables:
                schema = table.schema or "<unspecified>"
                print(f"✅ Creating table: {schema}.{table.name}")

            from sqlalchemy import MetaData
            tmp = MetaData()
            tmp._schemas = {"core", "nfl", "market"}
            for table in all_tables:
                table.to_metadata(tmp)
            tmp.create_all(sync_conn)

        await conn.run_sync(sync_create_all)

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init())