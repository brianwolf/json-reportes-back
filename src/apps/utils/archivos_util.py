import os
from uuid import UUID

import apps.configs.variables as var
from apps.configs.loggers import get_logger
from apps.models.errores import AppException

_DIRECTORIO_SISTEMA_ARCHIVOS = var.get('DIRECTORIO_SISTEMA_ARCHIVOS')


def ruta_archivo(tipo_carpeta_value: str, nombre_carpeta: str,
                 nombre_archivo: str) -> str:
    '''
    Devuelve la ruta completa del archivo
    '''
    return ruta_tipo_carpeta(tipo_carpeta_value,
                             nombre_carpeta) + nombre_archivo


def ruta_tipo_carpeta(tipo_carpeta_value: str, nombre_carpeta: str) -> str:
    '''
    Devuelve la ruta completa del archivo
    '''
    return f'{ruta_carpeta(nombre_carpeta)}/{tipo_carpeta_value}/'


def ruta_carpeta(nombre_carpeta: str) -> str:
    '''
    Devuelve la ruta completa del archivo
    '''
    return ruta_completa(_DIRECTORIO_SISTEMA_ARCHIVOS, nombre_carpeta)


def nombre_con_extension(nombre: str, extension: ''):
    '''
    Devuelve el nombre con su extension, en caso de no tenerla la agrega,
    en caso de que ya la tiene, devuelve el nombre sin cambios
    '''
    if not nombre.endswith('.' + extension):
        nombre += '.' + extension

    return nombre


def guardar_archivo(directorio: str, nombre: str, contenido: bytes):
    '''
    Guarda un archivo en el directorio indicado, en caso de que no exista la crea
    '''
    crear_directorio_si_no_existe(directorio)

    with open(ruta_completa(directorio, nombre), 'wb+') as archivo_python:
        archivo_python.write(contenido)


def obtener_archivo(directorio: str, nombre: str) -> bytes:
    '''
    Recupera el contenido de un archivo con el nombre y en el directorio indicados
    '''
    with open(directorio + nombre, 'rb') as archivo:
        contenido = archivo.read()

    return contenido


def ruta_completa(directorio: str, nombre: str):
    '''
    Devuelve la ruta completa de un directorio y un nombre de archivo validando debidamente
    '''
    if not directorio.endswith('/'):
        directorio += '/'

    return directorio + nombre


def listado_archivos(directorio: str) -> list:
    '''
    Comando 'ls' de linux sobre el directorio
    '''
    return os.listdir(directorio)


def listado_archivos_directorio_base() -> list:
    '''
    Comando 'ls' de linux sobre el directorio base del sistema de archivos
    '''
    crear_directorio_si_no_existe(_DIRECTORIO_SISTEMA_ARCHIVOS)
    return os.listdir(_DIRECTORIO_SISTEMA_ARCHIVOS)


def crear_directorio_si_no_existe(directorio: str):
    '''
    Crea un directorio en caso de no existir
    '''
    if not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)


def borrar_archivo(directorio: str, nombre: str):
    '''
    Borra un archivo ubicada en la ruta enviada
    '''
    ruta_completa = directorio + nombre
    if os.path.exists(ruta_completa):
        os.remove(ruta_completa)
