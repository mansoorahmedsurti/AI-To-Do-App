from typing import Optional
from sqlmodel import Session, select
from app.models.user import User, UserCreate
from app.core.auth import hash_password


def create_user(*, session: Session, user_create: UserCreate) -> User:
    # With Better Auth, password hashing might be handled by the auth system
    # But we still need to hash passwords for direct user creation
    db_user = User.model_validate(
        user_create, update={"password_hash": hash_password(user_create.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(*, session: Session, user_id: str) -> Optional[User]:
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()