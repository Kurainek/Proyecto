"""Funciones de estadísticas (versión en español).
Punto de integración con la UI para mostrar top productos y totales.
"""

from typing import List


def top_productos(sesion, limite: int = 5) -> List[dict]:
    # Placeholder: devolver datos de ejemplo
    return [
        {"nombre": "Hamburguesa", "ventas": 10},
        {"nombre": "Pollo frito", "ventas": 8},
    ][:limite]


def total_ventas(sesion) -> float:
    return 12345.67
