from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash

from uuid import UUID

def select_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def select_user_by_id(db: Session, user_id: UUID) -> User:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_in: UserCreate):
    hashed_pwd = get_password_hash(user_in.password)
    
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_pwd 
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user