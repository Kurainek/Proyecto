"""Script de verificación de imports para el repo.
Intenta importar módulos clave y muestra errores con traceback.
"""
import importlib
import traceback

MODULOS = [
    'manejador_errores',
    'gestor_cache',
    'base_datos',
    'estadisticas',
    'utilidades',
    'BoletaFacade',
    'Menu_catalog',
    'menu_pdf',
    'ctk_pdf_viewer',
    'Ingrediente',
    'Stock',
    'Pedido',
    'ElementoMenu',
    'IMenu',
    'crud.boleta_crud',
    'crud.cliente_crud',
    'crud.ingrediente_crud',
    'crud.menu_crud',
    'crud.pedido_crud',
]

resultados = {}
for mod in MODULOS:
    try:
        importlib.import_module(mod)
        resultados[mod] = ("OK", None)
    except Exception:
        resultados[mod] = ("ERROR", traceback.format_exc())

print('Resumen de imports:')
errores = 0
for mod, (estado, info) in resultados.items():
    if estado == 'OK':
        print(f'  OK   - {mod}')
    else:
        errores += 1
        print(f'  ERROR - {mod}')

if errores:
    print('\nDetalles de errores:\n')
    for mod, (estado, info) in resultados.items():
        if estado != 'OK':
            print(f'--- {mod} ---')
            print(info)

exit(1 if errores else 0)
