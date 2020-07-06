import os

import yaml
from apps.configs.variables.ambiente import parsear_variables_de_ambiente
from apps.configs.variables.claves import Variable, _no_mostrar

__version__ = '1.2.1'

_variables_predefinidas = {}
_ruta_archivo_variables_predefinidas = 'imports/config/variables_predefinidas.env'


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

    with open(_ruta_archivo_variables_predefinidas, 'r') as archivo:
        renglones_archivo = archivo.readlines()

    for renglon in renglones_archivo:

        if renglon.startswith('#') or renglon == '\n':
            continue

        clave, valor = renglon.split('=')

        if '#' in valor:
            valor = valor[:valor.index('#')].strip()

        _variables_predefinidas[clave] = valor.replace('\n', '')

    _variables_predefinidas = parsear_variables_de_ambiente(
        _variables_predefinidas)


cargar_variables_predefinidas()
