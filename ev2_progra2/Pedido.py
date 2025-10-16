from ElementoMenu import CrearMenu 
class Pedido:
    def __init__(self):
        self.menus = []  

    def agregar_menu(self, menu: CrearMenu):

        for m in self.menus:
            if m.nombre == menu.nombre:
                m.cantidad += 1  
                return
        menu.cantidad = 1  
        self.menus.append(menu)

    def eliminar_menu(self, nombre_menu: str):
        for m in self.menus:
            if m.nombre == nombre_menu:
                if m.cantidad > 1:
                    m.cantidad -= 1
                else:
                    self.menus.remove(m)
                return

    def mostrar_pedido(self):
        lista = []
        for m in self.menus:
            subtotal = m.precio * m.cantidad
            lista.append((m.nombre, m.cantidad, m.precio, subtotal))
        return lista
       
    def calcular_total(self) -> float:
        total = 0
        for m in self.menus:
            total += m.precio * m.cantidad
        return total
