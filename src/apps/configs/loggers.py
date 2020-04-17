import logging
import os

import apps.configs.lector_variables as var
from apps.configs.variables import Variable

__version__ = '1.0.1'

_DIRECTORIO_LOGS = var.dame(Variable.DIRECTORIO_LOGS)
_NOMBRE_LOG_PREDEFINIDO = var.dame(Variable.NOMBRE_LOG_PREDEFINIDO)
_NIVEL_LOGS = var.dame(Variable.NIVEL_LOGS)

_loggers = {}


def get_logger(nombre=_NOMBRE_LOG_PREDEFINIDO) -> logging.Logger:
    '''
    Devuelve un objeto logger por un nombre, en caso de que no exista lo crea
    '''
    if nombre in _loggers.keys():
        return _loggers[nombre]

    if not os.path.exists(_DIRECTORIO_LOGS):
        os.makedirs(_DIRECTORIO_LOGS, exist_ok=True)

    logger = logging.getLogger(nombre)
    logger.setLevel(_NIVEL_LOGS)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    sh = logging.StreamHandler()
    sh.setLevel(_NIVEL_LOGS)
    sh.setFormatter(formatter)

    fh = logging.FileHandler(_DIRECTORIO_LOGS + f"{nombre}.log")
    fh.setLevel(_NIVEL_LOGS)
    fh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.addHandler(fh)

    _loggers[nombre] = logger

    return logger
