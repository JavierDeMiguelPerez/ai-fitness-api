# app/api/routers/diets.py
from app.api.deps import get_current_user
from app.models.diet import SavedDietPlan, DailyMealLog
from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.services import llm_service
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.diet import DietPlan, MealLogRequest, MealMacrosResponse, DietModificationRequest, DietPlanSave, MealLogSaveRequest, MealLogSaveResponse
from app.schemas.profile import UserProfileResponse

router = APIRouter(prefix="/diets", tags=["Diets"])

@router.post("/generate", response_model=DietPlan)
def generate_diet(current_user: User = Depends(get_current_user)):
    if not current_user.profile:
        raise HTTPException(status_code=400, detail="Profile not found. Please create one.")
        
    profile_dict = {
        "age": current_user.profile.age,
        "weight_kg": current_user.profile.weight_kg,
        "height_cm": current_user.profile.height_cm,
        "gender": current_user.profile.gender,
        "primary_goal": current_user.profile.primary_goal,
        "activity_level": current_user.profile.activity_level,
        "dietary_preferences": current_user.profile.dietary_preferences,
        "allergies": current_user.profile.allergies
    }
    
    diet_plan_dict = llm_service.generate_diet_plan(profile_dict)
    
    return diet_plan_dict

@router.post("/log-text", response_model=MealMacrosResponse)
def log_meal_from_text(request: MealLogRequest):
    macros_dict = llm_service.analyze_meal_text(request.meal_text)
    
    return macros_dict

@router.post("/modify", response_model=DietPlan)
def modify_diet(request: DietModificationRequest):
    current_plan_dict = request.current_plan.model_dump()
    
    modified_plan_dict = llm_service.modify_diet_plan(
        current_plan=current_plan_dict,
        modification_prompt=request.modification_prompt
    )
    
    return modified_plan_dict

@router.post("/save")
def save_diet_plan(request: DietPlanSave, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan_dict = request.plan.model_dump()
    
    new_plan = SavedDietPlan(
        user_id=current_user.id,
        name=request.plan.plan_name,
        plan_data=plan_dict
    )
    
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    
    return {"message": "Dieta guardada con éxito", "plan_id": new_plan.id}

@router.post("/log", response_model=MealLogSaveResponse)
def log_meal_and_save(request: MealLogSaveRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    macros_dict = llm_service.analyze_meal_text(request.meal_text)
    
    safe_calories = int(round(float(macros_dict["calories"])))
    safe_protein = int(round(float(macros_dict["protein_g"])))
    safe_carbs = int(round(float(macros_dict["carbs_g"])))
    safe_fats = int(round(float(macros_dict["fats_g"])))
    
    new_log = DailyMealLog(
        user_id=current_user.id,
        food_recognized=macros_dict["food_recognized"],
        calories=safe_calories,
        protein_g=safe_protein,
        carbs_g=safe_carbs,
        fats_g=safe_fats
    )
    
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    return {
        "message": "Comida registrada con éxito",
        "log_id": new_log.id,
        "food_recognized": macros_dict["food_recognized"],
        "calories": safe_calories,
        "protein_g": safe_protein,
        "carbs_g": safe_carbs,
        "fats_g": safe_fats
    }