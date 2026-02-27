# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FitnessAPI"
    PROJECT_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"

# Instanciamos la clase para poder importarla en otros archivos
settings = Settings()