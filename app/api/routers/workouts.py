# app/api/routers/workouts.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.workout import ExerciseLog, ExerciseLog, SetLog, WorkoutSession
from app.models.workout import SetLog
from app.schemas.tracking import WorkoutSessionCreate
from app.schemas.workout import UserProfile, WorkoutPlan
from app.services import llm_service
router = APIRouter(prefix="/workouts", tags=["Workouts"])

@router.post("/generate", response_model=WorkoutPlan)
def generate_workout(profile: UserProfile):
    profile_dict = profile.model_dump()
    
    workout_plan_dict = llm_service.generate_fitness_plan(profile_dict)
    
    return workout_plan_dict

@router.post("/log")
def log_workout_session(session_in: WorkoutSessionCreate, db: Session = Depends(get_db)):
    new_session = WorkoutSession(
        user_id=session_in.user_id, 
        day_name=session_in.day_name
    )
    
    for exc_in in session_in.exercises:
        new_exc = ExerciseLog(exercise_name=exc_in.exercise_name)
        
        for set_in in exc_in.sets:
            new_set = SetLog(
                set_number=set_in.set_number,
                reps=set_in.reps,
                weight_kg=set_in.weight_kg
            )
            new_exc.sets.append(new_set) 
            
        new_session.exercises.append(new_exc) 
        
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return {
        "message": "Entrenamiento registrado con éxito", 
        "session_id": new_session.id
    }