'''
Variables
---------

Utiliza un archivo .env para crear un diccionario usado como variables del proyecto, 
en caso de que exista la variable de ambiente en el sistema utiliza esa, 
en caso de que no, usa la del archivo 
'''
import os
from enum import Enum
from typing import Any, Dict, List

from logic.libs.variables.src import config


def iniciar(modulos: List[Any]):
    '''
    Configura la util, es requerido que los modulos que se le pasen tengan los siguientes atributos:

    - Variables: Enum -> enums con las claves para obtener las variables
    - no_mostrar: List[str] -> lista con las claves que se muestran en el metodo variables_cargadas()
    - ruta_archivo: str -> ruta del archivo .env con las variables del proyecto
    '''
    for clase in modulos:

        from logic.libs.variables.src.archivo import crear_diccionario_de_variables

        nuevas_variables = crear_diccionario_de_variables(clase.ruta_archivo)
        config._VARIABLES_PREDEFINIDAS.update(nuevas_variables)

        config._LISTA_ENUMS.extend(clase.Variable)
        config._NO_MOSTRAR.extend(clase.no_mostrar)


def dame(variable: Enum) -> str:
    '''
    Obtiene el valor de la variable de entorno correspondiente, en caso de no obtenerla,
    la saca del diccionario de variables predefinidas
    '''
    valor_de_diccionario = config._VARIABLES_PREDEFINIDAS.get(variable.value)
    return os.environ.get(variable.value, valor_de_diccionario)


def variables_cargadas() -> Dict[str, str]:
    '''
    Devuelve el mapa de variables con sus valores instanciados y filtrados por la lista de no mostrados
    '''
    return {
        clave.value: dame(clave)
        for clave in config._LISTA_ENUMS
        if clave.value not in config._NO_MOSTRAR
    }
