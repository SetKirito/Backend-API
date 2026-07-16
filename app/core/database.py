import os
from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    yield
