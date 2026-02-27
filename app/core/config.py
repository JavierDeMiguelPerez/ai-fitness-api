# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

# Instanciamos la clase para poder importarla en otros archivos
settings = Settings()