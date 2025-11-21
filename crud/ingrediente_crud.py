"""CRUD helpers for Ingrediente (placeholder)."""

from typing import Any


def create_ingrediente(session: Any, data: dict) -> dict:
    return {"status": "created", "ingrediente": data}


def list_ingredientes(session: Any) -> list:
    return []
