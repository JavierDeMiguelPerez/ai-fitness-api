# app/api/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.models.profile import UserProfile
from app.schemas.profile import UserProfileUpdate, UserProfileResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_service.select_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = user_service.create_user(db, user_in)
    return new_user



@router.get("/me", response_model=UserProfileResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    if not current_user.profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please create one.")
    return current_user.profile

@router.put("/me", response_model=UserProfileResponse)
def update_user_profile(
    profile_in: UserProfileUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    profile = current_user.profile
    if not profile:
        profile = UserProfile(user_id=current_user.id, **profile_in.model_dump())
        db.add(profile)
    else:
        for key, value in profile_in.model_dump().items():
            setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    return profile