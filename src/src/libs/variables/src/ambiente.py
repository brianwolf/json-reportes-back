import os
import re
from typing import Dict

_REGEX_EXTRAER_VARIABLE = r'\$\{[^\}]+\:*[^\}]*\}'
_REGEX_TIENE_VARIABLE = r'[^\$]*' + _REGEX_EXTRAER_VARIABLE + r'[^\$]*'


def _es_variable_de_ambiente(variable: str) -> bool:
    '''
    Debuelve verdadero si la variable tiene el formato 
    de una variable de ambiente
    '''
    return re.match(_REGEX_TIENE_VARIABLE, str(variable)) != None


def _parsear_variable_de_ambiente(variable: str) -> str:
    '''
    Obtiene el valor de la variable de entorno con el formato de ${VAR:default}
    '''
    if not _es_variable_de_ambiente(variable):
        return variable

    for variable_ambiente in re.findall(_REGEX_EXTRAER_VARIABLE, variable):

        var_y_default = variable_ambiente.replace(
            '${', '').replace('}', '').split(':', 1)

        var_ambiente = var_y_default[0]
        val_default = var_y_default[1] if len(var_y_default) > 1 else ''

        valor_final = os.environ.get(var_ambiente, val_default)

        variable = variable.replace(variable_ambiente, valor_final)

    return variable


def parsear_variables_de_ambiente(elemento: Dict[str, str]) -> Dict[str, str]:
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
