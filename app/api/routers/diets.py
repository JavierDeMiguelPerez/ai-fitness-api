# app/api/routers/diets.py
from fastapi import APIRouter
from app.schemas.diet import DietProfile, DietPlan
from app.services import llm_service

router = APIRouter(prefix="/diets", tags=["Diets"])

@router.post("/generate", response_model=DietPlan)
def generate_diet(profile: DietProfile):
    profile_dict = profile.model_dump()
    
    diet_plan_dict = llm_service.generate_diet_plan(profile_dict)
    
    return diet_plan_dict