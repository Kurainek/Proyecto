"""Ejemplo de patrón Método Plantilla (versión en español)."""

from abc import ABC, abstractmethod


class Documento(ABC):
    def generar(self):
        self.preparar()
        contenido = self.generar_contenido()
        self.finalizar()
        return contenido

    def preparar(self):
        pass

    @abstractmethod
    def generar_contenido(self):
        pass

    def finalizar(self):
        pass


class Boleta(Documento):
    def generar_contenido(self):
        return "Contenido de la boleta"
