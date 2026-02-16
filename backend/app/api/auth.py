from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime, timedelta

from app.models.user import User, UserCreate
from app.models.session import Session as SessionModel
from app.db.database import get_session
from app.core.auth import hash_password, verify_password

router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register")
def register_user(user_data: RegisterRequest, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create new user
    user = User(
        email=user_data.email,
        password_hash=hashed_password,
        name=user_data.name or user_data.email.split('@')[0]  # Use email prefix as name if not provided
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a session token for the new user
    session_token = str(uuid.uuid4())
    session_record = SessionModel(
        token=session_token,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(days=30)  # 30-day expiry
    )
    
    session.add(session_record)
    session.commit()

    return {"message": "User registered successfully", "user_id": user.id, "access_token": session_token}


@router.post("/login")
def login_user(login_data: LoginRequest, session: Session = Depends(get_session)):
    # Find user by email
    user = session.exec(select(User).where(User.email == login_data.email)).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create a session token
    session_token = str(uuid.uuid4())
    session_record = SessionModel(
        token=session_token,
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(days=30)  # 30-day expiry
    )
    
    session.add(session_record)
    session.commit()

    return {"access_token": session_token, "token_type": "bearer", "user_id": user.id}