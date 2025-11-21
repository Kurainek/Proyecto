from typing import List

from ElementoMenu import CrearMenu


class Pedido:
    """Representa un pedido que contiene varios menús y sus cantidades."""

    def __init__(self) -> None:
        self.menus: List[CrearMenu] = []

    def agregar_menu(self, menu: CrearMenu) -> None:
        """Agrega un menú al pedido; si ya existe, incrementa su cantidad."""
        for m in self.menus:
            if m.nombre.strip().lower() == menu.nombre.strip().lower():
                m.cantidad += 1
                return

        menu.cantidad = int(menu.cantidad) if menu.cantidad else 1
        if menu.cantidad <= 0:
            menu.cantidad = 1
        self.menus.append(menu)

    def eliminar_menu(self, nombre_menu: str) -> None:
        nombre_norm = nombre_menu.strip().lower()
        for m in list(self.menus):
            if m.nombre.strip().lower() == nombre_norm:
                if getattr(m, "cantidad", 0) > 1:
                    m.cantidad -= 1
                else:
                    self.menus.remove(m)
                return

    def mostrar_pedido(self):
        lista = []
        for m in self.menus:
            subtotal = float(m.precio) * int(m.cantidad)
            lista.append((m.nombre, m.cantidad, m.precio, subtotal))
        return lista

    def calcular_total(self) -> float:
        total = 0.0
        for m in self.menus:
            total += float(m.precio) * int(m.cantidad)
        return float(total)
