from enum import Enum
from typing import Any, Dict, List

_variables_predefinidas: Dict[str, str] = {}

_lista_enums: List[Enum] = []
_no_mostrar: List[str] = []


def init(clases_variables: List[Any]):
    '''
    '''
    global _variables_predefinidas, _no_mostrar, _lista_enums

    for clase in clases_variables:

        from apps.utils.variables.lector import crear_diccionario_de_variables

        nuevas_variables = crear_diccionario_de_variables(clase.ruta_archivo)
        _variables_predefinidas.update(nuevas_variables)

        _lista_enums.extend(clase.Variables)
        _no_mostrar.extend(clase.no_mostrar)
