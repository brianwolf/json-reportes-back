import os
from enum import Enum
from typing import Dict

import yaml

from apps.utils.variables.ambiente import parsear_variables_de_ambiente
from apps.utils.variables.init import _variables_predefinidas


def dame(variable: Enum) -> str:
    '''
    Obtiene el valor de la variable de entorno correspondiente, en caso de no obtenerla,
    la saca del diccionario de variables predefinidas
    '''
    valor_de_diccionario = _variables_predefinidas.get(variable.value)
    return os.environ.get(variable.value, valor_de_diccionario)


# def variables_cargadas() -> Dict[str, str]:
#     '''
#     Devuelve el mapa de variables con sus valores instanciados y filtrados por la lista de no mostrados
#     '''
#     resultado = {}

#     for clase_enum in _lista_enums:
#         resultado.update({
#             clave: dame(clase_enum(clave))
#             for clave in clase_enum.__members__.keys()
#             if clave not in _no_mostrar
#         })

#     return resultado


def _crear_diccionario_por_archivo_env(ruta_archivo: str) -> Dict[str, str]:
    '''
    '''
    with open(ruta_archivo, 'r') as archivo:
        renglones_archivo = archivo.readlines()

    diccionario_variables = {}
    for renglon in renglones_archivo:

        if renglon.startswith('#') or renglon == '\n':
            continue

        clave, valor = renglon.split('=')

        if '#' in valor:
            valor = valor[:valor.index('#')].strip()

        diccionario_variables[clave] = valor.replace('\n', '')

    return diccionario_variables


def crear_diccionario_de_variables(ruta_archivo: str) -> Dict[str, str]:
    '''
    Genera un diccionario con las variables del archivo enviado por 
    parametro parseadas con sus respectivas variables de ambiente
    '''
    variables_predefinidas = _crear_diccionario_por_archivo_env(ruta_archivo)
    return parsear_variables_de_ambiente(variables_predefinidas)
