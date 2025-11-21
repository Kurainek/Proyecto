"""Gestor de cache simple con TTL 
Uso: aplicar el decorador `cached(ttl=60)` sobre funciones que quieran ser memorizadas.
"""

import time
from functools import wraps


_cache = {}


def cached(ttl: int = 60):
    def decorador(func):
        @wraps(func)
        def envoltura(*args, **kwargs):
            clave = (func.__name__, args, tuple(sorted(kwargs.items())))
            entrada = _cache.get(clave)
            ahora = time.time()
            if entrada and ahora - entrada[0] < ttl:
                return entrada[1]
            valor = func(*args, **kwargs)
            _cache[clave] = (ahora, valor)
            return valor

        return envoltura

    return decorador


def estadisticas_cache():
    return {"entradas": len(_cache)}
