# app/api/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import user_service
import secrets
from datetime import datetime, timedelta
from app.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest
from app.schemas.common import MessageResponse
from app.schemas.token import Token
from app.core.security import verify_password, create_access_token, get_password_hash

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_service.select_user_by_email(db, email=form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": str(user.id), "email": str(user.email)})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = user_service.select_user_by_email(db, email=request.email)
    if not user:
        # For security, don't reveal if user exists. 
        # But for this simulation, we'll just return success.
        return {"message": "Si el email existe, se ha enviado un token"}
    
    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    
    # In a real app, send email here. 
    # For now, we return it to help the user test.
    return {
        "message": "Token generado (simulación de email)",
        "token": token
    }

@router.post("/reset-password", response_model=MessageResponse)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    from app.models.user import User # Local import to avoid circular dependency if any
    user = db.query(User).filter(
        User.reset_token == request.token,
        User.reset_token_expires > datetime.utcnow()
    ).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    
    user.hashed_password = get_password_hash(request.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    
    return {"message": "Contraseña actualizada con éxito"}