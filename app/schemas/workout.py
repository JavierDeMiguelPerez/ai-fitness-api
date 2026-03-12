# app/schemas/workout.py
from pydantic import BaseModel
from typing import List, Union
from typing import Optional

class UserProfile(BaseModel):
    age: int
    weight_kg: float
    height_cm: float
    gender: str
    experience_level: str
    primary_goal: str

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