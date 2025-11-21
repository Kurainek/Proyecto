from dataclasses import dataclass, field
from typing import List, Optional

from Ingrediente import Ingrediente
from Stock import Stock
from IMenu import IMenu


@dataclass
class CrearMenu(IMenu):
    nombre: str
    ingredientes: List[Ingrediente]
    precio: float = 0.0
    icono_path: Optional[str] = None
    cantidad: int = field(default=0, compare=False)

    def esta_disponible(self, stock: Stock) -> bool:
        for req in self.ingredientes:
            disponible = False
            req_nombre = req.nombre.strip().lower()
            req_unidad = req.unidad.strip().lower() if req.unidad else None

            for ing in stock.lista_ingredientes:
                ing_nombre = ing.nombre.strip().lower()
                ing_unidad = ing.unidad.strip().lower() if ing.unidad else None

                if ing_nombre == req_nombre and (
                    req_unidad is None or ing_unidad == req_unidad
                ):
                    try:
                        if float(ing.cantidad) >= float(req.cantidad):
                            disponible = True
                            break
                    except Exception:
                        # datos no numéricos, ignorar este ingrediente
                        continue

            if not disponible:
                return False

        return True

    def preparar(self, stock: Stock) -> None:
        for req in self.ingredientes:
            req_nombre = req.nombre.strip().lower()
            req_unidad = req.unidad.strip().lower() if req.unidad else None

            for ing in stock.lista_ingredientes:
                ing_nombre = ing.nombre.strip().lower()
                ing_unidad = ing.unidad.strip().lower() if ing.unidad else None

                if ing_nombre == req_nombre and (
                    req_unidad is None or ing_unidad == req_unidad
                ):
                    try:
                        ing.cantidad = float(ing.cantidad) - float(req.cantidad)
                        if ing.cantidad < 0:
                            ing.cantidad = 0
                    except Exception:
                        # si hay datos inválidos, evitamos romper la preparación
                        pass

                    break
