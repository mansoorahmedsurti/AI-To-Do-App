from datetime import datetime
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from uuid import UUID
from passlib.context import CryptContext

from app.models.user import User
from app.models.session import Session as SessionModel
from app.db.database import get_session

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme to extract token from Authorization header
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Extract the token from the authorization header
    session_token = token.credentials
    
    if not session_token:
        raise credentials_exception
    
    # Query the session table to validate the session token from Better Auth
    session_query = select(SessionModel).where(SessionModel.token == session_token)
    db_session = session.exec(session_query).first()
    
    if not db_session or db_session.expires_at < datetime.utcnow():
        raise credentials_exception
    
    # Get the user associated with this session
    user_query = select(User).where(User.id == db_session.user_id)
    user = session.exec(user_query).first()
    
    if not user:
        raise credentials_exception
    
    return user