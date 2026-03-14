# app/api/deps.py
import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.services import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
            
        user_id_uuid = uuid.UUID(user_id_str)
            
    except (jwt.InvalidTokenError, ValueError):
        raise credentials_exception
        
    user = user_service.select_user_by_id(db, user_id=user_id_uuid)
    if user is None:
        raise credentials_exception
        
    return user