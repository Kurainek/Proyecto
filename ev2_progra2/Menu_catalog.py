# menu_catalog.py
from typing import List
from ElementoMenu import CrearMenu
from Ingrediente import Ingrediente
from IMenu import IMenu

def get_default_menus() -> List[IMenu]:
    return [
        CrearMenu(
            "Papas Fritas",
            [
                Ingrediente("Papas","unid", 5),
            ],
            precio=500,
            icono_path="IMG/papasfritas.png",
        ),
        CrearMenu(
            "Pepsi",
            [
                Ingrediente("Pepsi","unid", 1),
            ],
            precio=1100,
            icono_path="IMG/Pepsi.png",
        ),
        CrearMenu(
            "Completo",
            [
                Ingrediente("Vienesa","unid", 1),
                Ingrediente("Pan de completo","unid", 1),
                Ingrediente("Tomate","unid", 1),
                Ingrediente("Palta","unid", 1),
            ],
            precio=1800,
            icono_path="IMG/completo.png",
        ),
        CrearMenu(
            "Hamburguesa",
            [
                Ingrediente("Pan de hamburguesa","unid", 1),
                Ingrediente("Lámina de queso","unid", 1),
                Ingrediente("Churrasco de carne","unid", 1),
            ],
            precio=3500,
            icono_path="IMG/hamburguesa.png",
        ),
        CrearMenu(
            "Panqueques",
            [
                Ingrediente("Panqueques","unid", 2),
                Ingrediente("Manjar","unid", 1),
                Ingrediente("Azúcar flor","unid", 1),
            ],
            precio=2000,
            icono_path="IMG/panqueques.png",
        ),
        CrearMenu(
            "Pollo frito",
            [
                Ingrediente("Presa de pollo","unid",1),
                Ingrediente("Porción de harina","unid", 1),
                Ingrediente("Porción de aceite","unid", 1),
            ],
            precio=2800,
            icono_path="IMG/pollofrito.png",
        ),
        CrearMenu(
            "Ensalada mixta",
            [
                Ingrediente("Lechuga","unid", 1),
                Ingrediente("Tomate","unid", 1),
                Ingrediente("Zanahoria rallada","unid", 1),
            ],
            precio=1500,
            icono_path="IMG/ensaladamixta.png",
        ),
    ]