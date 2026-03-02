# app/api/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service

# Creamos un router específico para usuarios
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Usar el servicio para buscar si existe
    existing_user = user_service.select_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Usar el servicio para crearlo
    new_user = user_service.insert_user(db, user_in)
    
    return new_user
