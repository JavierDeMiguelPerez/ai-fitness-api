from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from datetime import datetime
from app.core.database import Base

class SavedDietPlan(Base):
    __tablename__ = "saved_diet_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    plan_data = Column(JSON, nullable=False) # Aquí guardaremos la dieta entera de Llama 3
    created_at = Column(DateTime, default=datetime.utcnow)

class DailyMealLog(Base):
    __tablename__ = "daily_meal_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_recognized = Column(String, nullable=False) # Ej: "2 huevos y un plátano"
    calories = Column(Integer, nullable=False)
    protein_g = Column(Integer, nullable=False)
    carbs_g = Column(Integer, nullable=False)
    fats_g = Column(Integer, nullable=False)
    logged_at = Column(DateTime, default=datetime.utcnow)