import os
from apps.configs.mapa_variables import mapa_variables, no_mostrar


def get(variable: str) -> str:
    '''
    Obtiene el valor de la variable de entorno correspondiente, en caso de no obtenerla, 
    la saca del archivo de configuracion
    '''
    valor_de_diccionario = mapa_variables[variable]
    return os.environ.get(variable, valor_de_diccionario)


def variables_cargadas() -> dict:
    '''
    Devuelve el mapa de variables con sus valores instanciados y filtrados por la lista de no mostrados
    '''
    resultado = {}
    for key in mapa_variables.keys():
        if key in no_mostrar:
            continue

        resultado[key] = get(key)

    return resultado
