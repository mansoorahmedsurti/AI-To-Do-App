from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)


class User(UserBase, table=True):
    __tablename__ = "user"  # Explicit table name
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    
    # Relationships - using string references to avoid circular import issues
    todos: List["Todo"] = Relationship(back_populates="user", sa_relationship_args={"cascade": "all, delete-orphan"})
    conversations: List["Conversation"] = Relationship(back_populates="conversation_user", sa_relationship_args={"cascade": "all, delete-orphan"})


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: uuid.UUID

    class Config:
        from_attributes = True