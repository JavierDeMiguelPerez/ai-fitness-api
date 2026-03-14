import os
import sys

# Add the app directory to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models.user import User
from app.models.profile import UserProfile
from app.models.diet import SavedDietPlan, DailyMealLog
from app.models.workout import WorkoutPlan, WorkoutSession, ExerciseLog, SetLog

def recreate_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating all tables with UUIDs...")
    Base.metadata.create_all(bind=engine)
    
    print("Database recreation complete.")

if __name__ == "__main__":
    recreate_database()
