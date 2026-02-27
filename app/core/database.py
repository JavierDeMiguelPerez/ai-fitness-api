# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Creamos el motor conectándolo a la URL de Neon
engine = create_engine(settings.DATABASE_URL)

# 2. Creamos la fábrica de sesiones
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 3. Creamos la clase base para nuestros modelos
Base = declarative_base()

# 4. Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()