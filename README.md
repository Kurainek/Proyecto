# Proyecto
Proyecto de programación 2, sobre el control de un restaurante

## Notas rápidas

- **Ignorados por Git**: el repositorio ahora ignora `__pycache__/`, `.vscode/` y `venv/` vía `.gitignore`.
- **Logs**: los registros de la app se guardan en `restaurante.log`.

## Setup CRUD / Base de datos

La parte CRUD y la configuración de la base de datos están documentadas en `README_CRUD.md`.
Sigue ese archivo para crear el entorno virtual, configurar la base de datos y ejecutar el seed de ejemplo.

## Utilidades funcionales

He añadido `functional_tools.py` con ejemplos y utilidades que usan `filter`, `iter`,
`lambda`, list comprehensions, `map`, `reduce`, y `yield`. Hay tests básicos en
`tests/test_functional_tools.py` y puedes ejecutar `pytest` para verificarlos.
