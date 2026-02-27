# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # TODO: Define aquí PROJECT_NAME como string
    # TODO: Define aquí PROJECT_VERSION como string

    class Config:
        env_file = ".env"

# Instanciamos la clase para poder importarla en otros archivos
settings = Settings()