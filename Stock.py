from typing import List, Optional

from Ingrediente import Ingrediente


class Stock:
    """Contenedor simple de ingredientes y operaciones sobre el stock."""

    def __init__(self) -> None:
        self.lista_ingredientes: List[Ingrediente] = []

    def agregar_ingrediente(self, ingrediente: Ingrediente) -> None:
        """Agrega un ingrediente al stock.

        Si ya existe (nombre+unidad), suma cantidades.
        """
        nombre_norm = ingrediente.nombre.strip().lower()
        unidad_norm = ingrediente.unidad.strip().lower() if ingrediente.unidad else None

        for ing in self.lista_ingredientes:
            ing_nombre = ing.nombre.strip().lower()
            ing_unidad = ing.unidad.strip().lower() if ing.unidad else None
            if ing_nombre == nombre_norm and ing_unidad == unidad_norm:
                ing.cantidad += ingrediente.cantidad
                return

        self.lista_ingredientes.append(ingrediente)

    def eliminar_ingrediente(
        self,
        nombre_ingrediente: str,
        unidad: Optional[str] = None,
    ) -> bool:
        """Elimina un ingrediente por nombre (y opcionalmente unidad).

        Devuelve True si se eliminó.
        """
        nombre_norm = nombre_ingrediente.strip().lower()
        unidad_norm = unidad.strip().lower() if unidad else None

        for ing in list(self.lista_ingredientes):
            ing_nombre = ing.nombre.strip().lower()
            ing_unidad = ing.unidad.strip().lower() if ing.unidad else None
            if ing_nombre == nombre_norm and (
                unidad_norm is None or ing_unidad == unidad_norm
            ):
                self.lista_ingredientes.remove(ing)
                return True
        return False

    def verificar_stock(self) -> bool:
        return len(self.lista_ingredientes) > 0

    def actualizar_stock(
        self,
        nombre_ingrediente: str,
        nueva_cantidad: float,
        unidad: Optional[str] = None,
    ) -> bool:
        nombre_norm = nombre_ingrediente.strip().lower()
        unidad_norm = unidad.strip().lower() if unidad else None

        for ing in self.lista_ingredientes:
            ing_nombre = ing.nombre.strip().lower()
            ing_unidad = ing.unidad.strip().lower() if ing.unidad else None
            if ing_nombre == nombre_norm and (
                unidad_norm is None or ing_unidad == unidad_norm
            ):
                ing.cantidad = float(nueva_cantidad)
                return True
        return False

    def obtener_elementos_menu(self) -> List[Ingrediente]:
        return self.lista_ingredientes
