from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid


# Conversation Model
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"  # Explicit table name
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships - using string references to avoid circular import issues
    messages: List["Message"] = Relationship(back_populates="conversation", sa_relationship_args={"cascade": "all, delete-orphan"})
    conversation_user: "User" = Relationship(back_populates="conversations")


# Message Model
class Message(SQLModel, table=True):
    __tablename__ = "messages"  # Explicit table name
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id")
    role: str  # "user", "assistant", "tool"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: Optional[str] = None  # JSON string of tool calls
    tool_responses: Optional[str] = None  # JSON string of tool responses
    
    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")


# Extended Message model for creation (without ID)
class MessageCreate(SQLModel):
    conversation_id: Optional[uuid.UUID] = None  # Will be generated if None
    role: str
    content: str
    tool_calls: Optional[str] = None
    tool_responses: Optional[str] = None


# Extended Conversation model for creation (without ID)
class ConversationCreate(SQLModel):
    title: str
    user_id: uuid.UUID


# Response models - separate classes to avoid inheritance issues with SQL relationships
class ConversationResponse(SQLModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime


class MessageResponse(SQLModel):
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: str
    content: str
    timestamp: datetime
    tool_calls: Optional[str] = None
    tool_responses: Optional[str] = None