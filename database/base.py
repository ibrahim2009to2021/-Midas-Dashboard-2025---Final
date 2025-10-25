# database/base.py (NEW FILE)

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# Define the database URL
DATABASE_URL = "sqlite:///./furniture.db"

# Create the engine and the Base here. This file has no local imports.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()