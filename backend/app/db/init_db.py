from sqlmodel import SQLModel
from app.db.database import engine
from app.models.user import User
from app.models.todo import Todo


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)