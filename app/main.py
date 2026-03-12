from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import auth, users, workouts, diets

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(diets.router)
app.include_router(auth.router)
@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "project_name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION
    }