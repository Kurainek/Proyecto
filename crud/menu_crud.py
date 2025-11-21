"""CRUD helpers for Menu (placeholder)."""

from typing import Any


def create_menu(session: Any, menu: dict) -> dict:
    return {"status": "created", "menu": menu}


def list_menus(session: Any) -> list:
    return []
