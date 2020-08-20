from enum import Enum
from typing import List

import logic.app.services.sistema_de_archivos_service as fs
from logic.libs.excepcion.excepcion import AppException
from logic.libs.variables.variables import dame
from logic.app.configs.variables import Variable
from logic.app.errors.modelos_errors import ArchivoErrors, ModelosErrors
from logic.app.models.modelos import Archivo, Modelo, TipoArchivo
from logic.app.repositories import archivo_repository
from logic.app.services import modelo_service


def listado_archivos(nombre_modelo: str, tipo: TipoArchivo) -> List[str]:
    '''
    Devuelve una lista con los nombres de todos los archivos de un modelo en la app
    '''
    resultado_modelo = modelo_service.buscar_por_filtros(
        {'NOMBRE': nombre_modelo})
    if not resultado_modelo:
        mensaje = f'El nombre modelo con nombre {nombre_modelo} no fue encontrado'
        raise AppException(ArchivoErrors.ARCHIVO_NO_EXISTE, mensaje)

    id_modelo = resultado_modelo[0].id
    return archivo_repository.listado_archivos(id_modelo, tipo)


def crear(a: Archivo) -> Archivo:
    '''
    Crea un archivo en la base de datos y en el sistema de archivos
    '''
    if archivo_repository.buscar_por_filtros({'NOMBRE': a.nombre}):
        mensaje = f'El nombre {a.nombre} ya esta en uso'
        raise AppException(ArchivoErrors.ARCHIVO_YA_EXISTENTE, mensaje)

    a = archivo_repository.crear(a)
    fs.crear(a)

    return a


def actualizar(a: Archivo) -> Archivo:
    '''
    Actualiza un archivo en la base de datos y en el sistema de archivos
    '''
    a_viejo = obtener(a.id)
    if not a_viejo:
        mensaje = f'El archivo con id {id} no fue encontrado'
        raise AppException(ArchivoErrors.ARCHIVO_NO_EXISTE, mensaje)

    fs.borrar(a_viejo)

    a = archivo_repository.actualizar(a)
    fs.crear(a)


def borrar(id: any):
    """
    Borra un archivo en la base de datos y en el sistema de archivos buscando por nombre
    """
    a = obtener(id)
    if not a:
        mensaje = f'El archivo con id {id} no fue encontrado'
        raise AppException(ArchivoErrors.ARCHIVO_NO_EXISTE, mensaje)

    archivo_repository.borrar(id)
    fs.borrar(a)


def obtener_por_nombre(nombre_modelo: str, nombre_archivo: str, contenidos_tambien: bool = False) -> Archivo:
    '''
    Obtiene un archivo de la base de datos y del sistema de archivos
    '''
    m = modelo_service.obtener_por_nombre(nombre_modelo)
    if not m:
        mensaje = f'El modelo con nombre {nombre_modelo} no fue encontrado'
        raise AppException(ModelosErrors.MODELO_NO_EXISTE, mensaje)

    a = m.buscar_archivo(nombre_archivo)
    if not a:
        mensaje = f'El archivo con nombre {nombre_archivo} no fue encontrado'
        raise AppException(ArchivoErrors.ARCHIVO_NO_EXISTE, mensaje)

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

    return fs.obtener(a)


def actualizar_contenido(a: Archivo):
    '''
    Actualiza el contenido de un arhivo
    '''
    if not a:
        return None

    fs.borrar(a)
    fs.crear(a)
