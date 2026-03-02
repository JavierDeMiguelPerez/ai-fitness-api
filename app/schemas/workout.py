# app/schemas/workout.py
from pydantic import BaseModel
from typing import List

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