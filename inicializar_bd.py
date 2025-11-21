"""Script para inicializar la base de datos ."""
from base_datos import engine
try:
    from modelos import Base
except Exception:
    Base = None

if Base is not None:
    Base.metadata.create_all(bind=engine)
    print('Base de datos inicializada')
else:
    print('No se encontró modelos.Base; define modelos.py con SQLAlchemy Base')
