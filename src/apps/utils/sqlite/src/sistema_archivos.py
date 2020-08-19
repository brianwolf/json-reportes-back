import os

from apps.utils.sqlite.src.config import _RUTA_DB


def _crear_arbol_de_directorios():
    '''
    Crea el arbol de directorios necesario para que sqlite cree su archivo .db
    '''
    if os.path.exists(_RUTA_DB):
        return

    directorio = os.path.dirname(_RUTA_DB)
    os.makedirs(directorio, exist_ok=True)
