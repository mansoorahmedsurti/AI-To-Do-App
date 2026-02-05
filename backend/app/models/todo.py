from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional
import uuid


class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"  # low, medium, high
    due_date: Optional[date] = None
    category: Optional[str] = None
    user_id: uuid.UUID


class Todo(TodoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)


class TodoCreate(TodoBase):
    pass


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    category: Optional[str] = None


class TodoResponse(TodoBase):
    id: uuid.UUID
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True