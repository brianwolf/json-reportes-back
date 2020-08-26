from typing import Dict

from logic.libs.variables.src.ambiente import parsear_variables_de_ambiente


def _crear_diccionario_por_archivo_env(ruta_archivo: str) -> Dict[str, str]:
    """
    """
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
    """
    Genera un diccionario con las variables del archivo enviado por 
    parametro parseadas con sus respectivas variables de ambiente
    """
    variables_predefinidas = _crear_diccionario_por_archivo_env(ruta_archivo)
    return parsear_variables_de_ambiente(variables_predefinidas)
