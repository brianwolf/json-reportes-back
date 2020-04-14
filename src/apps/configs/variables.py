from enum import Enum


class Variable(Enum):
    VERSION = 'VERSION'
    PYTHON_HOST = 'PYTHON_HOST'
    PYTHON_PORT = 'PYTHON_PORT'
    NIVEL_LOGS = 'NIVEL_LOGS'
    DIRECTORIO_LOGS = 'DIRECTORIO_LOGS'
    NOMBRE_LOG_PREDEFINIDO = 'NOMBRE_LOG_PREDEFINIDO'
    NOMBRE_LOG_REST = 'NOMBRE_LOG_REST'
    DIRECTORIO_SISTEMA_ARCHIVOS = 'DIRECTORIO_SISTEMA_ARCHIVOS'


_predefinidas = {
    'VERSION': 'local',
    'PYTHON_HOST': 'localhost',
    'PYTHON_PORT': 5000,
    'NIVEL_LOGS': 'INFO',
    'DIRECTORIO_LOGS': 'resources/logs/',
    'NOMBRE_LOG_PREDEFINIDO': 'app',
    'NOMBRE_LOG_REST': 'rest',
    'DIRECTORIO_SISTEMA_ARCHIVOS': 'resources/templates'
}

_no_mostrar = []
