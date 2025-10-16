from Ingrediente import Ingrediente

class Stock:
    def __init__(self):
        self.lista_ingredientes = []

    def agregar_ingrediente(self, ingrediente: Ingrediente):
        for ing in self.lista_ingredientes:
            if ing.nombre == ingrediente.nombre and ing.unidad == ingrediente.unidad:
                ing.cantidad += ingrediente.cantidad
                return
        self.lista_ingredientes.append(ingrediente) #en caso de que no exusta

    def eliminar_ingrediente(self, nombre_ingrediente: str, unidad: str = None):
        for ing in self.lista_ingredientes:
            if ing.nombre == nombre_ingrediente and (unidad is None or ing.unidad == unidad):
                self.lista_ingredientes.remove(ing)
                break

    def verificar_stock(self) -> bool:
        return len(self.lista_ingredientes) > 0

    def actualizar_stock(self, nombre_ingrediente: str, nueva_cantidad: float, unidad: str = None):
        for ing in self.lista_ingredientes:
            if ing.nombre == nombre_ingrediente and (unidad is None or ing.unidad == unidad):
                ing.cantidad = nueva_cantidad
                break

    def obtener_elementos_menu(self):
        return self.lista_ingredientes