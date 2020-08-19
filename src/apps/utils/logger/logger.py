'''
Logger
-------

Crea logs de la aplicacion
'''
import logging

from apps.utils.logger.src.archivo import crear_log
from apps.utils.logger.src.config import (_DIRECTORIO_LOGS, _LOGGERS,
                                          _NIVEL_LOGS)


def iniciar(directorio: str, nivel: str):
    '''
    Configura el logger para el proyecto
    '''
    _DIRECTORIO_LOGS = directorio
    _NIVEL_LOGS = nivel


def log(nombre: str = 'app') -> logging.Logger:
    '''
    Devuelve un objeto logger por un nombre, en caso de que no exista lo crea
    '''
    if nombre not in _LOGGERS:
        _LOGGERS[nombre] = crear_log(nombre)

    return _LOGGERS[nombre]
