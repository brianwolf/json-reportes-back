'''
Crea logs para la aplicacion
'''
import logging
import os

from apps.utils.logger.init import _directorio_logs, _nivel_logs

_loggers = {}


def log(nombre: str = 'app') -> logging.Logger:
    '''
    Devuelve un objeto logger por un nombre, en caso de que no exista lo crea
    '''
    global _loggers

    if nombre in _loggers:
        return _loggers[nombre]

    if not os.path.exists(_directorio_logs):
        os.makedirs(_directorio_logs, exist_ok=True)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    sh = logging.StreamHandler()
    sh.setLevel(_nivel_logs)
    sh.setFormatter(formatter)

    ruta_log = os.path.join(_directorio_logs, f'{nombre}.log')
    fh = logging.FileHandler(ruta_log)
    fh.setLevel(_nivel_logs)
    fh.setFormatter(formatter)

    logger = logging.getLogger(nombre)
    logger.setLevel(_nivel_logs)
    logger.addHandler(sh)
    logger.addHandler(fh)

    _loggers[nombre] = logger

    return logger
