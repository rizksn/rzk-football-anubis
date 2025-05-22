from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine

metadata = MetaData(schema="nfl")

# Loaded via .env DATABASE_URL
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)