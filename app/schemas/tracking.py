# app/schemas/tracking.py
from pydantic import BaseModel
from typing import List

class SetLogCreate(BaseModel):
    set_number: int
    reps: int
    weight_kg: float

class ExerciseLogCreate(BaseModel):
    exercise_name: str
    sets: List[SetLogCreate]

class WorkoutSessionCreate(BaseModel):
    user_id: int
    day_name: str
    exercises: List[ExerciseLogCreate]