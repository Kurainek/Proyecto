"""Manejador de errores y excepciones del proyecto (español)."""

from functools import wraps


class ProyectoError(Exception):
    """Error base para excepciones del proyecto."""


class ErrorValidacion(ProyectoError):
    """Excepción para errores de validación en la aplicación."""


class ErrorStock(ProyectoError):
    """Excepción relacionada con problemas de stock."""


def manejar_errores(func=None):
    """Decorador para capturar y mostrar errores controlados.

    Se puede usar como `@manejar_errores` o como `@manejar_errores()`.
    """

    def decorator(f):
        @wraps(f)
        def envoltura(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except ProyectoError as e:
                # Loguear o mostrar según necesidad; por ahora print para consola
                print(f"Error del proyecto: {e}")
            except Exception as e:
                print(f"Error no esperado: {e}")

        return envoltura

    # Si se usa sin paréntesis: @manejar_errores
    if callable(func):
        return decorator(func)

    # Si se usa con paréntesis: @manejar_errores()
    return decorator
