from enum import Enum
from typing import List

import apps.utils.archivos_util as archivos_util
from apps.configs.variables.lector import Variable, dame
from apps.models.errores import AppException
from apps.models.modelos import Archivo, Modelo, TipoArchivo
from apps.repositories import archivo_repository, modelo_repository


class Errores(Enum):
    NOMBRE_EN_USO = 'NOMBRE_EN_USO'
    MODELO_NO_EXISTE = 'MODELO_NO_EXISTE'


def listado_archivos(nombre_modelo: str) -> List[str]:
    '''
    Devuelve una lista con los nombres de todos los archivos de un modelo en la app
    '''
    resultado_modelo = modelo_repository.buscar_por_filtros(
        {'NOMBRE': nombre_modelo})
    if not resultado_modelo:
        mensaje = f'El nombre modelo con nombre {nombre_modelo} no fue encontrado'
        raise AppException(Errores.MODELO_NO_EXISTE, mensaje)

    id_modelo = resultado_modelo[0].id
    return archivo_repository.listado_archivos(id_modelo)


# def crear(m: Modelo) -> Modelo:
#     '''
#     Crea un modelo en la base de datos y en el sistema de archivos,
#     devuelve el id del modelo y los ids de los archivos generados
#     '''
#     if modelo_repository.buscar_por_nombre(m.nombre):
#         mensaje = f'El nombre {m.nombre} ya esta en uso'
#         raise AppException(Errores.NOMBRE_EN_USO, mensaje)

#     m = modelo_repository.crear(m)
#     dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)

#     for a in m.archivos:
#         directorio_absoluto = a.directorio_absoluto(dir_base)
#         archivos_util.crear(directorio_absoluto, a.nombre, a.contenido)

#     return m


# def actualizar(m: Modelo) -> None:
#     '''
#     Actualiza una modelo en la base de datos y en el sistema de archivos
#     '''
#     m_viejo = obtener(m.id)
#     if not m_viejo:
#         mensaje = f'El modelo con id {m.id} no fue encontrado'
#         raise AppException(Errores.MODELO_NO_EXISTE, mensaje)

#     archivos_a_borrar = [
#         archivo for archivo in m_viejo.archivos
#         if archivo not in m.archivos
#     ]
#     archivos_a_crear = [
#         archivo for archivo in m.archivos
#         if archivo not in m_viejo.archivos
#     ]

#     m = modelo_repository.actualizar(m)

#     dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)

#     for a in archivos_a_borrar:
#         directorio_absoluto = a.directorio_absoluto(dir_base)
#         archivos_util.borrar(directorio_absoluto, a.nombre)

#     for archivo in archivos_a_crear:
#         directorio_absoluto = a.directorio_absoluto(dir_base)
#         archivos_util.crear(dir_base, a.nombre, a.contenido)


# def borrar_por_nombre(nombre: str):
#     """
#     Borra una modelo en la base de datos y en el sistema de archivos buscando por nombre
#     """
#     m = modelo_repository.buscar_por_nombre(nombre)
#     if not m:
#         mensaje = f'El modelo con nombre {nombre} no fue encontrado'
#         raise AppException(Errores.MODELO_NO_EXISTE, mensaje)

#     modelo_repository.borrar(m.id)

#     dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)
#     for a in m.archivos:
#         archivos_util.borrar(a.directorio_absoluto(dir_base), a.nombre)


def obtener_por_nombre(nombre_modelo: str, nombre_archivo: str, contenidos_tambien: bool = False) -> Archivo:
    '''
    Obtiene un archivo de la base de datos y del sistema de archivos
    '''
    m = modelo_repository.buscar_por_nombre(nombre_modelo)
    if not m:
        mensaje = f'El nombre modelo con nombre {nombre_modelo} no fue encontrado'
        raise AppException(Errores.MODELO_NO_EXISTE, mensaje)

    a = m.buscar_archivo(nombre_archivo)

    if contenidos_tambien:
        return _cargar_contenido(a)
    return a


def obtener(id: int, contenidos_tambien: bool = False) -> Archivo:
    '''
    Obtiene un archivo de la base de datos y del sistema de archivos
    '''
    a = archivo_repository.buscar(id)
    if contenidos_tambien:
        return _cargar_contenido(a)

    return a


def _cargar_contenido(a: Archivo) -> Archivo:
    '''
    Obtiene los contenidos de los arhivos
    '''
    if not a:
        return None

    dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)

    directorio_absoluto = a.directorio_absoluto(dir_base)
    a.contenido = archivos_util.obtener(directorio_absoluto, a.nombre)

    return a
