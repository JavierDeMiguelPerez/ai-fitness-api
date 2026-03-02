# app/schemas/workout.py
from pydantic import BaseModel
from typing import List

class UserProfile(BaseModel):
    age: int
    weight_kg: float
    height_cm: float
    gender: str
    experience_level: str
    primary_goal: str

class Exercise(BaseModel):
    name: str
    sets: int
    reps: str
    rest_seconds: int
    

class WorkoutDay(BaseModel):
    day_name: str
    exercises: List[Exercise]

class WorkoutPlan(BaseModel):
    plan_name: str
    goal: str
    days: List[WorkoutDay]