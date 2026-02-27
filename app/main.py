# app/main.py
from fastapi import FastAPI
from app.core.config import settings # <-- Importamos los settings

app = FastAPI()

@app.get("/health")
def health_check() -> dict:
    # TODO: Modifica el return para que devuelva el status "ok",
    # el "project_name" leyendo de settings, y 
    # la "version" leyendo de settings.
    pass