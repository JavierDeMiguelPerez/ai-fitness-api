# app/api/routers/workouts.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.workout import ExerciseLog, ExerciseLog, SetLog, WorkoutSession
from app.models.workout import SetLog
from app.schemas.tracking import WorkoutSessionCreate, WorkoutSessionResponse
from app.schemas.workout import UserProfile, WorkoutModificationRequest, WorkoutPlan
from app.services import llm_service
from typing import List
from app.models.workout import WorkoutPlan as DBWorkoutPlan
from app.schemas.workout import WorkoutPlanSave
from app.api.deps import get_current_user
from app.models.user import User
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

@router.get("/history/{user_id}", response_model=List[WorkoutSessionResponse])
def get_workout_history(user_id: int, db: Session = Depends(get_db)):
    # Hacemos la query filtrando por el usuario y ordenando por fecha descendente
    history = db.query(WorkoutSession)\
                .filter(WorkoutSession.user_id == user_id)\
                .order_by(WorkoutSession.date.desc())\
                .all()
    
    return history

@router.post("/modify", response_model=WorkoutPlan)
def modify_workout(request: WorkoutModificationRequest):
    current_plan_dict = request.current_plan.model_dump()
    
    modified_plan_dict = llm_service.modify_fitness_plan(
        current_plan=current_plan_dict, 
        modification_prompt=request.modification_prompt
    )
    
    return modified_plan_dict

@router.post("/save")
def save_workout_plan(request: WorkoutPlanSave, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan_dict = request.plan.model_dump()
    
    new_plan = DBWorkoutPlan(
        user_id=current_user.id,
        name=request.plan.plan_name,
        plan_data=plan_dict
    )
    
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    
    return {"message": "Rutina guardada con éxito", "plan_id": new_plan.id}