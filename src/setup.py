import sqlite3

from apps.configs.lector_variables import dame
from apps.configs.variables import Variable

_RUTA_ARCHIVO_BD_SQLITE = dame(Variable.DB_SQLITE_RUTA)
_RUTA_ARCHIVO_SCRIPT = dame(Variable.DB_SQLITE_SCRIPT)


def iniciar_db(script: str):
    '''
    Crea la base de datos de SQLite mediante el script
    '''
    conn = sqlite3.connect(_RUTA_ARCHIVO_BD_SQLITE)

    c = conn.cursor()
    c.executescript(script)

    conn.commit()
    conn.close()


with open(_RUTA_ARCHIVO_SCRIPT, mode='r') as script_archivo:
    iniciar_db(script_archivo.read())
