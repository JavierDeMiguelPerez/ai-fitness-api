# app/schemas/diet.py
from pydantic import BaseModel
from typing import List, Optional


class Meal(BaseModel):
    meal_name: str
    description: str
    calories: int
    protein_g: int
    carbs_g: int
    fats_g: int

class DailyDiet(BaseModel):
    day_name: str # Ej: "Monday"
    total_calories: int
    meals: List[Meal]

class DietPlan(BaseModel):
    plan_name: str
    goal: str
    days: List[DailyDiet]

class MealLogRequest(BaseModel):
    meal_text: str

class MealMacrosResponse(BaseModel):
    food_recognized: str
    calories: int
    protein_g: int
    carbs_g: int
    fats_g: int

class DietModificationRequest(BaseModel):
    current_plan: DietPlan
    modification_prompt: str

class DietPlanSave(BaseModel):
    plan: DietPlan

class MealLogSaveRequest(BaseModel):
    meal_text: str

class MealLogSaveResponse(BaseModel):
    message: str
    log_id: int
    food_recognized: str
    calories: int
    protein_g: int
    carbs_g: int
    fats_g: int