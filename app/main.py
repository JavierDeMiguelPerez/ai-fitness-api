# app/main.py
from fastapi import FastAPI
from app.core.config import settings # <-- Importamos los settings

app = FastAPI()

@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "project_name": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION
    }