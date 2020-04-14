import os

from apps.configs.variables import Variable, _no_mostrar, _predefinidas

__version__ = '1.1.1'


def dame(variable: Variable) -> str:
    '''
    Obtiene el valor de la variable de entorno correspondiente, en caso de no obtenerla, 
    la saca del archivo de configuracion
    '''
    valor_de_diccionario = _predefinidas.get(variable.value)
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
