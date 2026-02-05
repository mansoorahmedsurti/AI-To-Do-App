from sqlmodel import create_engine, Session
from app.core.config import settings
from typing import Generator
import os

# Database URL for PostgreSQL - MUST be provided as environment variable
# For testing purposes only: Allow SQLite if TESTING environment variable is set
if settings.DATABASE_URL:
    engine = create_engine(settings.DATABASE_URL)
elif os.getenv("TESTING"):
    # ONLY for testing without Docker - NOT for production
    engine = create_engine("sqlite:///./test_todo_app.db")
else:
    raise ValueError("DATABASE_URL environment variable is required. No SQLite fallback allowed in production.")


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session