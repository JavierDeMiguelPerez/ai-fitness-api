from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

def select_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def select_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def insert_user(db: Session, user_in: UserCreate) -> User:
    new_user = User(
        email=user_in.email,
        hashed_password=user_in.password + "fakehash",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
