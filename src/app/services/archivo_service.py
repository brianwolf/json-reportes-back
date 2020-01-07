import os
import shutil
from uuid import UUID
from enum import Enum

import app.configs.variables as var
import app.utils.archivos_util as util
from app.configs.loggers import get_logger
from app.models.carpeta import Archivo, Carpeta, TipoCarpeta
from app.models.errores import AppException


class Errores(Enum):
    RUTA_NO_EXISTE = 'RUTA_NO_EXISTE'


def guardar_archivo(carpeta: Carpeta, archivo: Archivo):
    '''
    Crea el arachivo en el sistema de archivos, la estructura que maneja
    es:

    {carpeta.nombre}/{carpeta.tipo}/{archivo.nombre}

    IMPORTANTE: el nombre debe incluir la extension del archivo
    '''
    directorio = util.ruta_tipo_carpeta(carpeta.tipo.value, carpeta.nombre)
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    ruta = util.ruta_archivo(
        carpeta.tipo.value, carpeta.nombre, archivo.nombre)

    with open(ruta, 'wb+') as archivo_python:
        archivo_python.write(archivo.contenido)


def obtener_contenido_por_nombre(carpeta: Carpeta, nombre: str) -> bytes:
    '''
    Devuelve el contenido del archivo
    '''
    ruta = util.ruta_archivo(carpeta.tipo.value, carpeta.nombre, nombre)
    _validar_existencia_ruta(ruta)
    return obtener_contenido(ruta)


def obtener_contenido_por_tipo_y_nombre(tipo: TipoCarpeta, nombre_carpeta: str, nombre_archivo: str) -> bytes:
    '''
    Devuelve el contenido del archivo
    '''
    ruta = util.ruta_archivo(tipo.value, nombre_carpeta, nombre_archivo)
    _validar_existencia_ruta(ruta)
    return obtener_contenido(ruta)


def obtener_contenido(ruta_completa: str) -> bytes:
    '''
    Devuelve el contenido del archivo por su ruta completa
    '''
    _validar_existencia_ruta(ruta_completa)
    with open(ruta_completa, 'rb') as archivo:
        contenido = archivo.read()

    return contenido


def borrar_contenido(carpeta: Carpeta, nombre: str):
    '''
    Elimina el archivo del sistema de archivos
    '''
    ruta = util.ruta_archivo(carpeta.tipo.value, carpeta.nombre, nombre)
    _validar_existencia_ruta(ruta)
    os.remove(ruta)


def borrar_contenido_por_tipo(tipo: TipoCarpeta, nombre_carpeta: str, nombre_archivo: str):
    '''
    Elimina el archivo del sistema de archivos
    '''
    ruta = util.ruta_archivo(tipo.value, nombre_carpeta, nombre_archivo)
    _validar_existencia_ruta(ruta)
    os.remove(ruta)


def borrar_tipo_carpeta(tipo: TipoCarpeta, nombre_carpeta: str):
    '''
    Elimina el archivo del sistema de archivos
    '''
    ruta = util.ruta_tipo_carpeta(tipo.value, nombre_carpeta)
    _validar_existencia_ruta(ruta)
    shutil.rmtree(ruta, ignore_errors=False, onerror=None)


def borrar_carpeta_y_archivos(carpeta: Carpeta):
    '''
    Elimina la carpeta con todos sus archivos
    '''
    ruta = util.ruta_carpeta(carpeta.nombre)
    _validar_existencia_ruta(ruta)
    shutil.rmtree(ruta, ignore_errors=False, onerror=None)


def reemplazar_archivo(carpeta: Carpeta, archivo_nuevo: Archivo):
    '''
    Reemplaza el contenido del archivo
    '''
    borrar_contenido(carpeta, archivo_nuevo.nombre)
    guardar_archivo(carpeta, archivo_nuevo)


def _validar_existencia_ruta(ruta: str):
    if not os.path.exists(ruta):
        mensaje = f'La rura {ruta} NO existe'
        raise AppException(Errores.RUTA_NO_EXISTE, mensaje)
