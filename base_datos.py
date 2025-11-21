"""Helpers para conectar a la base de datos (versión en español)."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

URL_BD = os.environ.get("DATABASE_URL", "sqlite:///proyecto.db")
engine = create_engine(URL_BD, echo=False)
SessionLocal = sessionmaker(bind=engine)


def obtener_sesion():
    return SessionLocal()
