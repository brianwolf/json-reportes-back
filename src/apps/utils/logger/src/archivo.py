import logging
import os

from apps.utils.logger.src.config import _DIRECTORIO_LOGS, _NIVEL_LOGS


def crear_log(nombre: str = 'app') -> logging.Logger:
    '''
    Devuelve un objeto logger por un nombre, en caso de que no exista lo crea
    '''

    if not os.path.exists(_DIRECTORIO_LOGS):
        os.makedirs(_DIRECTORIO_LOGS, exist_ok=True)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s (%(process)d) - %(levelname)s - %(message)s')

    sh = logging.StreamHandler()
    sh.setLevel(_NIVEL_LOGS)
    sh.setFormatter(formatter)

    ruta_log = os.path.join(_DIRECTORIO_LOGS, f'{nombre}.log')
    fh = logging.FileHandler(ruta_log)
    fh.setLevel(_NIVEL_LOGS)
    fh.setFormatter(formatter)

    logger = logging.getLogger(nombre)
    logger.setLevel(_NIVEL_LOGS)
    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger
