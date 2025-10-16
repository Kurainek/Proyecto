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
            for ing in stock.lista_ingredientes:
                if ing.nombre == req.nombre and (req.unidad is None or ing.unidad == req.unidad):
                    if int(ing.cantidad) >= int(req.cantidad):
                        disponible = True
                        break
            if not disponible:
                return False
        return True
    
    def preparar(self, stock: Stock) -> None:
        for req in self.ingredientes:
            for ing in stock.lista_ingredientes:
                if ing.nombre == req.nombre and (req.unidad is None or ing.unidad == req.unidad):
                    ing.cantidad = str(int(ing.cantidad) - int(req.cantidad))
                    break


