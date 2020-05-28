import os

import yaml
from apps.configs.variables.ambiente import parsear_variables_de_ambiente
from apps.configs.variables.claves import Variable, _no_mostrar

__version__ = '1.2.1'

_variables_predefinidas = {}
_ruta_archivo_variables_predefinidas = 'imports/config/variables_predefinidas.yml'


def dame(variable: Variable) -> str:
    '''
    Obtiene el valor de la variable de entorno correspondiente, en caso de no obtenerla,
    la saca del diccionario de variables predefinidas
    '''
    valor_de_diccionario = _variables_predefinidas.get(variable.value)
    return os.environ.get(variable.value, valor_de_diccionario)


def variables_cargadas() -> dict:
    '''
    Devuelve el mapa de variables con sus valores instanciados y filtrados por la lista de no mostrados
    '''
    return {
        clave: dame(Variable(clave))
        for clave in Variable.__members__.keys()
        if clave not in _no_mostrar
    }


def cargar_variables_predefinidas():
    '''
    Carga el diccionario de variables predefinidas de un archivo .yml
    '''
    global _variables_predefinidas

    if not os.path.exists(_ruta_archivo_variables_predefinidas):
        raise Exception(
            f'cargar_variables_predefinidas() -> yml de configuracion {_ruta_archivo_variables_predefinidas} no encontrado')

    with open(_ruta_archivo_variables_predefinidas) as params_yaml_archivo:
        params_yaml = yaml.safe_load(params_yaml_archivo)

    _variables_predefinidas = parsear_variables_de_ambiente(params_yaml)


cargar_variables_predefinidas()
