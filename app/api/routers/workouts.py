# app/api/routers/workouts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.workout import ExerciseLog, SetLog, WorkoutSession
from app.schemas.tracking import WorkoutSessionCreate, WorkoutSessionResponse, WorkoutSessionUpdate
from app.schemas.workout import WorkoutModificationRequest, WorkoutPlan, WorkoutPlanSave, SavedWorkoutPlanResponse, WorkoutLogResponse, WorkoutSaveResponse
from app.schemas.common import MessageResponse
from app.schemas.profile import UserProfileResponse
from app.services import llm_service
from typing import List
from app.models.workout import WorkoutPlan as DBWorkoutPlan
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/workouts", tags=["Workouts"])

@router.get("/saved", response_model=List[SavedWorkoutPlanResponse])
def get_saved_workouts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    saved_plans = db.query(DBWorkoutPlan)\
                    .filter(DBWorkoutPlan.user_id == current_user.id)\
                    .order_by(DBWorkoutPlan.created_at.desc())\
                    .all()
    return saved_plans

@router.get("/active", response_model=SavedWorkoutPlanResponse)
def get_active_workout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    active_plan = db.query(DBWorkoutPlan).filter(
        DBWorkoutPlan.user_id == current_user.id,
        DBWorkoutPlan.is_active == True
    ).first()
    if not active_plan:
        raise HTTPException(status_code=404, detail="No hay rutina activa")
    return active_plan

@router.put("/saved/{plan_id}/activate", response_model=MessageResponse)
def activate_workout_plan(plan_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Deactivate all plans for this user
    db.query(DBWorkoutPlan).filter(DBWorkoutPlan.user_id == current_user.id).update({"is_active": False})
    # Activate the selected plan
    plan = db.query(DBWorkoutPlan).filter(DBWorkoutPlan.id == plan_id, DBWorkoutPlan.user_id == current_user.id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    plan.is_active = True
    db.commit()
    return {"message": "Rutina activada con éxito"}

@router.post("/generate", response_model=WorkoutPlan)
def generate_workout(current_user: User = Depends(get_current_user)):
    if not current_user.profile:
        raise HTTPException(status_code=400, detail="Profile not found. Please create one.")
        
    # Convert SQLAlchemy model to dict, exclude internal IDs for LLM if desired
    profile_dict = {
        "age": current_user.profile.age,
        "weight_kg": current_user.profile.weight_kg,
        "height_cm": current_user.profile.height_cm,
        "gender": current_user.profile.gender,
        "experience_level": current_user.profile.experience_level,
        "primary_goal": current_user.profile.primary_goal
    }
    
    workout_plan_dict = llm_service.generate_fitness_plan(profile_dict)
    
    return workout_plan_dict

@router.post("/log", response_model=WorkoutLogResponse)
def log_workout_session(session_in: WorkoutSessionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_session = WorkoutSession(
        user_id=current_user.id, 
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

@router.get("/history", response_model=List[WorkoutSessionResponse])
def get_workout_history(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Hacemos la query filtrando por el usuario y ordenando por fecha descendente
    history = db.query(WorkoutSession)\
                .filter(WorkoutSession.user_id == current_user.id)\
                .order_by(WorkoutSession.date.desc())\
                .offset(skip)\
                .limit(limit)\
                .all()
    
    return history

@router.post("/modify", response_model=WorkoutPlan)
def modify_workout(request: WorkoutModificationRequest, current_user: User = Depends(get_current_user)):
    current_plan_dict = request.current_plan.model_dump()
    
    modified_plan_dict = llm_service.modify_fitness_plan(
        current_plan=current_plan_dict, 
        modification_prompt=request.modification_prompt
    )
    
    return modified_plan_dict

@router.post("/save", response_model=WorkoutSaveResponse)
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

@router.delete("/saved/{plan_id}", response_model=MessageResponse)
def delete_saved_workout(plan_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = db.query(DBWorkoutPlan).filter(DBWorkoutPlan.id == plan_id, DBWorkoutPlan.user_id == current_user.id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    
    db.delete(plan)
    db.commit()
    return {"message": "Rutina eliminada con éxito"}

@router.put("/history/{session_id}", response_model=MessageResponse)
def update_workout_session(session_id: int, session_data: WorkoutSessionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id, WorkoutSession.user_id == current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    # Update flat fields
    session.day_name = session_data.day_name
    
    # Clear existing exercises (cascade delete-orphan will handle exercise_logs and set_logs)
    session.exercises.clear()
    
    # Add new content
    for exc_in in session_data.exercises:
        new_exc = ExerciseLog(exercise_name=exc_in.exercise_name)
        for set_in in exc_in.sets:
            new_set = SetLog(
                set_number=set_in.set_number,
                reps=set_in.reps,
                weight_kg=set_in.weight_kg
            )
            new_exc.sets.append(new_set)
        session.exercises.append(new_exc)
    
    db.commit()
    return {"message": "Sesión actualizada con éxito"}

@router.delete("/history/{session_id}", response_model=MessageResponse)
def delete_workout_session(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = db.query(WorkoutSession).filter(WorkoutSession.id == session_id, WorkoutSession.user_id == current_user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    
    db.delete(session)
    db.commit()
    return {"message": "Sesión eliminada con éxito"}