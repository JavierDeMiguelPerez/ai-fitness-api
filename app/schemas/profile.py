from pydantic import BaseModel
from typing import Optional

class UserProfileBase(BaseModel):
    age: int
    weight_kg: float
    height_cm: float
    gender: str
    experience_level: str
    primary_goal: str
    activity_level: Optional[str] = "None"
    dietary_preferences: Optional[str] = "None"
    allergies: Optional[str] = "None"

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(UserProfileBase):
    pass

from uuid import UUID

class UserProfileResponse(UserProfileBase):
    id: int
    user_id: UUID

    class Config:
        from_attributes = True
