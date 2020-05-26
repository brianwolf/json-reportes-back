from enum import Enum
from typing import List

import apps.utils.archivos_util as archivos_util
from apps.configs.variables.lector import Variable, dame
from apps.models.errors.app import AppException
from apps.models.modelos import Archivo, Modelo, TipoArchivo
from apps.repositories import archivo_repository, modelo_repository


class Errores(Enum):
    NOMBRE_EN_USO = 'NOMBRE_EN_USO'
    ARCHIVO_NO_EXISTE = 'MODELO_NO_EXISTE'
    ARCHIVO_YA_EXISTENTE = 'ARCHIVO_YA_EXISTENTE'


def listado_archivos(nombre_modelo: str) -> List[str]:
    '''
    Devuelve una lista con los nombres de todos los archivos de un modelo en la app
    '''
    resultado_modelo = modelo_repository.buscar_por_filtros(
        {'NOMBRE': nombre_modelo})
    if not resultado_modelo:
        mensaje = f'El nombre modelo con nombre {nombre_modelo} no fue encontrado'
        raise AppException(Errores.ARCHIVO_NO_EXISTE, mensaje)

    id_modelo = resultado_modelo[0].id
    return archivo_repository.listado_archivos(id_modelo)


def crear(a: Archivo) -> Archivo:
    '''
    Crea un archivo en la base de datos y en el sistema de archivos
    '''
    if archivo_repository.buscar_por_filtros({'NOMBRE': a.nombre}):
        mensaje = f'El nombre {a.nombre} ya esta en uso'
        raise AppException(Errores.ARCHIVO_YA_EXISTENTE, mensaje)

    a = archivo_repository.crear(a)

    dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)
    directorio_absoluto = a.directorio_absoluto(dir_base)
    archivos_util.crear(directorio_absoluto, a.nombre, a.contenido)

    return a


def actualizar(a: Archivo) -> Archivo:
    '''
    Actualiza un archivo en la base de datos y en el sistema de archivos
    '''
    a_viejo = obtener(a.id)
    if not a_viejo:
        mensaje = f'El archivo con id {id} no fue encontrado'
        raise AppException(Errores.ARCHIVO_NO_EXISTE, mensaje)

    dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)
    archivos_util.borrar(a_viejo.directorio_absoluto(dir_base), a_viejo.nombre)

    a = archivo_repository.actualizar(a)
    archivos_util.crear(a.directorio_absoluto(dir_base), a.nombre)


def borrar(id: Archivo):
    """
    Borra un archivo en la base de datos y en el sistema de archivos buscando por nombre
    """
    a = obtener(id)
    if not a:
        mensaje = f'El archivo con id {id} no fue encontrado'
        raise AppException(Errores.ARCHIVO_NO_EXISTE, mensaje)

    archivo_repository.borrar(id)

    dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)
    archivos_util.borrar(a.directorio_absoluto(dir_base), a.nombre)


def obtener_por_nombre(nombre_modelo: str, nombre_archivo: str, contenidos_tambien: bool = False) -> Archivo:
    '''
    Obtiene un archivo de la base de datos y del sistema de archivos
    '''
    m = modelo_repository.buscar_por_nombre(nombre_modelo)
    if not m:
        mensaje = f'El nombre modelo con nombre {nombre_modelo} no fue encontrado'
        raise AppException(Errores.ARCHIVO_NO_EXISTE, mensaje)

    a = m.buscar_archivo(nombre_archivo)

    if contenidos_tambien:
        a.contenido = obtener_contenido(a)
    return a


def obtener(id: int, contenidos_tambien: bool = False) -> Archivo:
    '''
    Obtiene un archivo de la base de datos y del sistema de archivos
    '''
    a = archivo_repository.buscar(id)
    if contenidos_tambien:
        a.contenido = obtener_contenido(a)

    return a


def obtener_contenido(a: Archivo) -> bytes:
    '''
    Obtiene los contenidos de los arhivos
    '''
    if not a:
        return None

    dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)

    directorio_absoluto = a.directorio_absoluto(dir_base)
    return archivos_util.obtener(directorio_absoluto, a.nombre)


def actualizar_contenido(a: Archivo):
    '''
    Actualiza el contenido de un arhivo
    '''
    if not a:
        return None

    dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)
    directorio_absoluto = a.directorio_absoluto(dir_base)

    archivos_util.borrar(directorio_absoluto, a.nombre)
    archivos_util.crear(directorio_absoluto, a.nombre, a.contenido)
