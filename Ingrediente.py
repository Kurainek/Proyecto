# Ingrediente.py
from dataclasses import dataclass
from typing import Optional

@dataclass(eq=True, frozen=False)
class Ingrediente:
    nombre: str
    unidad: Optional[str]  
    cantidad: float          

    def __post_init__(self):
        self.cantidad = float(self.cantidad)
        if self.cantidad <= 0:
            raise ValueError(f"La cantidad de '{self.nombre}' debe ser mayor a 0")
        if self.unidad:
            self.unidad = self.unidad.lower() 

    def __str__(self):
        if self.unidad:
            return f"{self.nombre} ({self.unidad}) x {self.cantidad}"
        return f"{self.nombre} x {self.cantidad}"