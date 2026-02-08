from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime


class Session(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    token: str = Field(unique=True, nullable=False)  # Session token from Better Auth
    user_id: uuid.UUID = Field(foreign_key="user.id")
    expires_at: datetime
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    

class SessionCreate(SQLModel):
    token: str
    user_id: uuid.UUID
    expires_at: datetime


class SessionResponse(SQLModel):
    id: uuid.UUID
    token: str
    user_id: uuid.UUID
    expires_at: datetime

    class Config:
        from_attributes = True