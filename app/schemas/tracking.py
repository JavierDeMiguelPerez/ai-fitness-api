# app/schemas/tracking.py
from pydantic import BaseModel
from typing import List
from datetime import datetime

class SetLogCreate(BaseModel):
    set_number: int
    reps: int
    weight_kg: float

class ExerciseLogCreate(BaseModel):
    exercise_name: str
    sets: List[SetLogCreate]

class WorkoutSessionCreate(BaseModel):
    day_name: str
    exercises: List[ExerciseLogCreate]

class SetLogResponse(BaseModel):
    id: int
    set_number: int
    reps: int
    weight_kg: float

    class Config:
        from_attributes = True

class ExerciseLogResponse(BaseModel):
    id: int
    exercise_name: str
    sets: List[SetLogResponse]

    class Config:
        from_attributes = True

class WorkoutSessionResponse(BaseModel):
    id: int
    user_id: int
    date: datetime
    day_name: str
    exercises: List[ExerciseLogResponse]

    class Config:
        from_attributes = True