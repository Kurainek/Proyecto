"""CRUD helpers for Pedido (placeholder)."""

from typing import Any


def create_pedido(session: Any, pedido: dict) -> dict:
    return {"status": "created", "pedido": pedido}


def list_pedidos(session: Any) -> list:
    return []
