from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///delivery.db")

# Create a DeclarativeMeta instance
Base = declarative_base()

