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

class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
