import logging
import os

from apps.configs.variables.claves import Variable
from apps.configs.variables.lector import dame

__version__ = '1.2.0'

_loggers = {}


def obtener_logger(nombre: str = 'app') -> logging.Logger:
    '''
    Devuelve un objeto logger por un nombre, en caso de que no exista lo crea
    '''
    if nombre in _loggers:
        return _loggers[nombre]

    directorio_logs = dame(Variable.DIRECTORIO_LOGS)
    nivel_logs = dame(Variable.NIVEL_LOGS)

    if not os.path.exists(directorio_logs):
        os.makedirs(directorio_logs, exist_ok=True)

    logger = logging.getLogger(nombre)
    logger.setLevel(nivel_logs)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    sh = logging.StreamHandler()
    sh.setLevel(nivel_logs)
    sh.setFormatter(formatter)

    ruta_log = os.path.join(directorio_logs, f'{nombre}.log')
    fh = logging.FileHandler(ruta_log)
    fh.setLevel(nivel_logs)
    fh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.addHandler(fh)

    _loggers[nombre] = logger

    return logger
