from enum import Enum
from importlib.util import module_from_spec, spec_from_file_location
from os import path

from apps.configs.lector_variables import dame
from apps.configs.loggers import get_logger
from apps.configs.variables import Variable

_RUTA_BASE_REPOSITORIO: str
_BD: TipoBD

_LOG = get_logger()


class TipoBD(Enum):
    ARCHIVO = 'archivo'
    SQLITE = 'sqlite'


def configurar_repos(bd: str, ruta_base_repositorios: str):
    '''
    '''
    global _RUTA_BASE_REPOSITORIO
    global _BD

    _RUTA_BASE_REPOSITORIO = path.join(ruta_base_repositorios, bd)
    _BD = TipoBD[bd]

    _LOG.info(f'Usando DB: {_BD} con REPO en: {_RUTA_BASE_REPOSITORIO}')


def crear_repo(nombre_modulo: str):
    '''
    Carga un repositorio dependiendo del repositorio
    '''
    ruta_archivo = path.join(
        _RUTA_BASE_REPOSITORIO, f'{nombre_modulo}.{dame(Variable.PYTHON_EXTENSION)}')

    spec = spec_from_file_location(nombre_modulo, ruta_archivo)
    modulo = module_from_spec(spec)
    spec.loader.exec_module(modulo)

    return modulo
