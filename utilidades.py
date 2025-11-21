"""Utilidades generales en español."""


def formatear_precio(valor: float) -> str:
    return f"${valor:,.2f}"


def limitar(valor, minimo, maximo):
    return max(minimo, min(valor, maximo))
