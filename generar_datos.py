"""Script para generar datos o reportes de ejemplo."""

import json
from pathlib import Path


CARPETA_REPORTES = Path("reportes")
CARPETA_REPORTES.mkdir(exist_ok=True)

muestra = [{"id": 1, "cliente": "Ana", "total": 1200}]
with open(CARPETA_REPORTES / "pedidos_generados.json", "w", encoding="utf-8") as f:
    json.dump(muestra, f, ensure_ascii=False, indent=2)

print("Reporte de ejemplo generado en", CARPETA_REPORTES / "pedidos_generados.json")
