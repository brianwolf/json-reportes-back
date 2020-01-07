import os
from app.configs.mapa_variables import mapa_variables


def get(variable: str) -> str:
    '''
    Obtiene el valor de la variable de entorno correspondiente, en caso de no obtenerla, 
    la saca del archivo de configuracion
    '''
    valor_de_diccionario = mapa_variables[variable]
    return os.environ.get(variable, valor_de_diccionario)
