"""CRUD helpers for Cliente (placeholder).
"""

from typing import Any


def create_cliente(session: Any, cliente: dict) -> dict:
    return {"status": "created", "cliente": cliente}


def list_clientes(session: Any) -> list:
    return []
