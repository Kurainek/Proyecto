"""Modelos SQLAlchemy.
Define tus entidades principales aquí.
"""

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Ingrediente(Base):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    cantidad = Column(Float, default=0.0)


class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, default=0.0)
