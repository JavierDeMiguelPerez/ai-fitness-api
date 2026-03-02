# app/api/routers/workouts.py
from fastapi import APIRouter
from app.schemas.workout import UserProfile, WorkoutPlan
from app.services import llm_service
router = APIRouter(prefix="/workouts", tags=["Workouts"])

@router.post("/generate", response_model=WorkoutPlan)
def generate_workout(profile: UserProfile):
    profile_dict = profile.model_dump()
    
    workout_plan_dict = llm_service.generate_fitness_plan(profile_dict)
    
    return workout_plan_dict
