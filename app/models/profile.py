from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    age = Column(Integer, nullable=False)
    weight_kg = Column(Float, nullable=False)
    height_cm = Column(Float, nullable=False)
    gender = Column(String, nullable=False)
    experience_level = Column(String, nullable=False)
    primary_goal = Column(String, nullable=False)
    
    # Optional fields for Diet
    activity_level = Column(String, nullable=True, default="None")
    dietary_preferences = Column(String, nullable=True, default="None")
    allergies = Column(String, nullable=True, default="None")
    
    user = relationship("User", back_populates="profile")
