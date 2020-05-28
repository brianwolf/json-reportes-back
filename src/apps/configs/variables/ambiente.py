import os
import re

_REGEX_AMBIENTE = '\\$[^\\}]+(:[^\\}])*\\}'


def parsear_variables_de_ambiente(elemento: dict) -> dict:
    '''
    Devuelve el diccionario con las variables de ambiente
    reemplazadas por su correspondiente valor
    '''
    if isinstance(elemento, dict):
        nuevo_d = {}
        for clave, valor in elemento.items():
            nuevo_d[clave] = parsear_variables_de_ambiente(valor)
        return nuevo_d

    if isinstance(elemento, list):
        return [
            parsear_variables_de_ambiente(elem)
            for elem in elemento
        ]

    return _parsear_variable_de_ambiente(elemento)


def _es_variable_de_ambiente(variable: str) -> bool:
    '''
    Debuelve verdadero si la variable tiene el formato 
    de una variable de ambiente
    '''
    return re.match(_REGEX_AMBIENTE, str(variable)) != None


def _parsear_variable_de_ambiente(variable: str) -> str:
    '''
    Obtiene el valor de la variable de entorno con el formato de ${VAR:default}
    '''
    if not _es_variable_de_ambiente(variable):
        return variable

    variables = variable.replace(
        '${', '').replace('}', '').split(':', 1)

    var_ambiente = variables[0]
    val_default = variables[1] if len(variables) > 1 else ''

    return obtener_valor(var_ambiente, val_default)


def obtener_valor(variable: str, valor_predefinido: str = '') -> str:
    '''
    Devuelve el valor de una variable de ambiente
    '''
    return os.environ.get(variable, valor_predefinido)
