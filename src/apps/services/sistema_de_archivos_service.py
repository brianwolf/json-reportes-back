from os import path

import apps.utils.archivos_util as archivos_util
from apps.configs.variables.lector import Variable, dame
from apps.models.modelos import Archivo, Modelo, TipoArchivo


def crear(a: Archivo):
    '''
    Crea un archivo en el sistema de archivos
    '''
    archivos_util.crear(obtener_directorio_absoluto(a), a.nombre, a.contenido)


def borrar(a: Archivo):
    """
    Borra un archivo en el sistema de archivos
    """
    archivos_util.borrar(obtener_directorio_absoluto(a), a.nombre)


def obtener(a: Archivo) -> bytes:
    '''
    Obtiene un archivo de la base de datos y del sistema de archivos
    '''
    return archivos_util.obtener(obtener_directorio_absoluto(a), a.nombre)


def obtener_directorio_absoluto(a: Archivo) -> str:
    '''
    Obtiene el directorio absoluto en donde esta guardado el archivo en el sistema de archivos
    '''
    dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)
    return path.join(dir_base, obtener_directorio_relativo(a))


def obtener_directorio_relativo(a: Archivo) -> str:
    '''
    Obtiene el directorio relativo en donde esta guardado el archivo en el sistema de archivos
    '''
    return path.join(str(a.tipo.value).lower(), str(a.id_modelo))
