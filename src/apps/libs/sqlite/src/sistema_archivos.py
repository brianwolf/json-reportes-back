import os


def _crear_arbol_de_directorios(ruta_archivo_sqlite: str):
    '''
    Crea el arbol de directorios necesario para que sqlite cree su archivo .db
    '''
    if os.path.exists(ruta_archivo_sqlite):
        return

    directorio = os.path.dirname(ruta_archivo_sqlite)
    os.makedirs(directorio, exist_ok=True)
