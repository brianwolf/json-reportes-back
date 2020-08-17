from enum import Enum
from typing import List

ruta_archivo: str = 'consume/config/variables_predefinidas.env'

no_mostrar: List[str] = ['NIVEL_LOGS']


class Variables(Enum):
    VERSION = 'VERSION'
    PYTHON_HOST = 'PYTHON_HOST'
    PYTHON_PORT = 'PYTHON_PORT'
    NIVEL_LOGS = 'NIVEL_LOGS'
    DIRECTORIO_LOGS = 'DIRECTORIO_LOGS'
    DIRECTORIO_SISTEMA_ARCHIVOS = 'DIRECTORIO_SISTEMA_ARCHIVOS'
    DIRECTORIO_TEMP = 'DIRECTORIO_TEMP'
    DB_SQLITE_SCRIPT = 'DB_SQLITE_SCRIPT'
    DB_SQLITE_RUTA = 'DB_SQLITE_RUTA'
    DB_TIPO = 'DB_TIPO'
