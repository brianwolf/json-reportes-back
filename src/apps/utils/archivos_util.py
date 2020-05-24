import os
from typing import List

__version__ = '1.0.0'


def nombre_con_extension(nombre: str, extension: ''):
    '''
    Devuelve el nombre con su extension, en caso de no tenerla la agrega,
    en caso de que ya la tiene, devuelve el nombre sin cambios
    '''
    if not nombre.endswith('.' + extension):
        nombre += '.' + extension

    return nombre


def crear(directorio: str, nombre: str, contenido: bytes):
    '''
    Guarda un archivo en el directorio indicado, en caso de que no exista la crea
    '''
    crear_directorio_si_no_existe(directorio)

    with open(os.path.join(directorio, nombre), 'wb+') as archivo_python:
        archivo_python.write(contenido)


def obtener(directorio: str, nombre: str) -> bytes:
    '''
    Recupera el contenido de un archivo con el nombre y en el directorio indicados
    '''
    with open(os.path.join(directorio, nombre), 'rb') as archivo:
        contenido = archivo.read()

    return contenido


def listado(directorio: str) -> List[str]:
    '''
    Comando 'ls' de linux sobre el directorio
    '''
    return os.listdir(directorio)


def crear_directorio_si_no_existe(directorio: str):
    '''
    Crea un directorio en caso de no existir
    '''
    if not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)


def borrar(directorio: str, nombre: str):
    '''
    Borra un archivo ubicada en la ruta enviada
    '''
    crear = os.path.join(directorio, nombre)
    if os.path.exists(crear):
        os.remove(crear)
