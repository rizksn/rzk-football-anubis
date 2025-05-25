from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Define engine
engine = create_async_engine(DATABASE_URL, echo=True)
async_engine = engine  

async_session = async_sessionmaker(engine, expire_on_commit=False)

metadata = MetaData(schema=None)  