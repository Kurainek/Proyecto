from dataclasses import dataclass
from typing import Optional


@dataclass(eq=True, frozen=False)
class Ingrediente:
    """Representa un ingrediente con nombre, unidad y cantidad.

    El `nombre` se normaliza (se recortan espacios) y la `unidad` se guarda
    en minúsculas si está presente. La cantidad debe ser un número >= 0.
    """

    nombre: str
    unidad: Optional[str]
    cantidad: float

    def __post_init__(self) -> None:
        self.nombre = str(self.nombre).strip()
        try:
            self.cantidad = float(self.cantidad)
        except Exception:
            raise ValueError(f"Cantidad inválida para '{self.nombre}': {self.cantidad}")

        if self.cantidad < 0:
            raise ValueError(f"La cantidad de '{self.nombre}' no puede ser negativa")

        if self.unidad:
            self.unidad = str(self.unidad).strip().lower()

    def __str__(self) -> str:
        if self.unidad:
            return f"{self.nombre} ({self.unidad}) x {self.cantidad}"
        return f"{self.nombre} x {self.cantidad}"
