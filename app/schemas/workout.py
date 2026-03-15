# app/schemas/workout.py
from pydantic import BaseModel
from typing import List, Union
from typing import Optional


class Exercise(BaseModel):
    name: str
    sets: Optional[Union[int, str]] = 0 
    reps: Optional[str] = ""
    rest_seconds: Optional[Union[int, str]] = 0
    

class WorkoutDay(BaseModel):
    day_name: str
    exercises: List[Exercise] = []

class WorkoutPlan(BaseModel):
    plan_name: str
    goal: str
    days: List[WorkoutDay]

class WorkoutModificationRequest(BaseModel):
    current_plan: WorkoutPlan
    modification_prompt: str

class WorkoutPlanSave(BaseModel):
    plan: WorkoutPlan

from datetime import datetime
from uuid import UUID

class SavedWorkoutPlanResponse(BaseModel):
    id: int
    user_id: UUID
    name: str
    plan_data: WorkoutPlan
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class WorkoutLogResponse(BaseModel):
    message: str
    session_id: int

class WorkoutSaveResponse(BaseModel):
    message: str
    plan_id: int