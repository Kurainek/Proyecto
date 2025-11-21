"""Funciones para cargar reportes."""

import json
from pathlib import Path


CARPETA_REPORTES = Path("reportes")


def cargar_pedidos(nombre_archivo: str):
    ruta = CARPETA_REPORTES / nombre_archivo
    if not ruta.exists():
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        if nombre_archivo.endswith(".json"):
            return json.load(f)
        return f.read()
