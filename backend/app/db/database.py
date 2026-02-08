from sqlmodel import create_engine, Session
from app.core.config import settings
from typing import Generator
import os

# Database URL for PostgreSQL - MUST be provided as environment variable
# NO SQLite fallbacks allowed - app must crash if DATABASE_URL is not set
if settings.DATABASE_URL:
    engine = create_engine(settings.DATABASE_URL)
else:
    raise ValueError("DATABASE_URL environment variable is required. No fallbacks allowed.")


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session