# app/models/workout.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    plan_data = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class WorkoutSession(Base):
    __tablename__ = "workout_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    day_name = Column(String)
    
    exercises = relationship("ExerciseLog", back_populates="session", cascade="all, delete-orphan")

class ExerciseLog(Base):
    __tablename__ = "exercise_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("workout_sessions.id"), nullable=False)
    exercise_name = Column(String, nullable=False)
    
    session = relationship("WorkoutSession", back_populates="exercises")
    
    sets = relationship("SetLog", back_populates="exercise", cascade="all, delete-orphan")

class SetLog(Base):
    __tablename__ = "set_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    exercise_log_id = Column(Integer, ForeignKey("exercise_logs.id"), nullable=False)
    set_number = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight_kg = Column(Float, nullable=False)
    
    exercise = relationship("ExerciseLog", back_populates="sets")