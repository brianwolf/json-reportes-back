from enum import Enum
from typing import List

import apps.utils.archivos_util as archivos_util
from apps.configs.variables.claves import Variable
from apps.configs.variables.lector import dame
from apps.models.errores import AppException
from apps.models.modelos import Archivo, Modelo, TipoArchivo
from apps.repositories import archivo_repository, modelo_repository


class Errores(Enum):
    NOMBRE_EN_USO = 'NOMBRE_EN_USO'


def listar_todas_los_modelos() -> List[str]:
    '''
    Devuelve una lista con los nombres de todas las modelos en la app
    '''
    return archivos_util.listado_archivos_directorio_base()


def crear(m: Modelo) -> Modelo:
    '''
    Crea un modelo en la base de datos y en el sistema de archivos,
    devuelve el id del modelo y los ids de los archivos generados
    '''
    if modelo_repository.buscar_por_nombre(m.nombre):
        mensaje = f'El nombre {m.nombre} ya esta en uso'
        raise AppException(Errores.NOMBRE_EN_USO, mensaje)

    m = modelo_repository.crear(m)
    dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)

    for a in m.archivos:
        directorio_absoluto = a.directorio_absoluto(dir_base)
        archivos_util.crear(directorio_absoluto, a.nombre, a.contenido)

    return m


def actualizar(m: Modelo) -> None:
    '''
    Actualiza una modelo en la base de datos y en el sistema de archivos
    '''
    m_viejo = obtener(m.id)

    archivos_a_borrar = [
        archivo for archivo in m_viejo.archivos
        if archivo not in m.archivos
    ]
    archivos_a_crear = [
        archivo for archivo in m.archivos
        if archivo not in m_viejo.archivos
    ]

    m = modelo_repository.actualizar(m)

    dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)

    for a in archivos_a_borrar:
        directorio_absoluto = a.directorio_absoluto(dir_base)
        archivos_util.borrar(directorio_absoluto, a.nombre)

    for archivo in archivos_a_crear:
        directorio_absoluto = a.directorio_absoluto(dir_base)
        archivos_util.crear(directorio_absoluto, a.nombre, a.contenido)


def borrar_por_nombre(nombre: str):
    """
    Borra una modelo en la base de datos y en el sistema de archivos buscando por nombre
    """
    m = modelo_repository.buscar_por_nombre(nombre)
    modelo_repository.borrar(m.id)


def obtener_por_nombre(nombre: str, contenidos_tambien: bool = False) -> Modelo:
    '''
    Obtiene una modelo de la base de datos y del sistema de archivos
    '''
    m = modelo_repository.buscar_por_nombre(nombre)
    if contenidos_tambien:
        m.archivos = [_cargar_contenido(a) for a in m.archivos]

    return m


def obtener(id: int, contenidos_tambien: bool = False) -> Modelo:
    '''
    Obtiene una modelo de la base de datos y del sistema de archivos
    '''
    m = modelo_repository.buscar(id)
    if contenidos_tambien:
        m.archivos = [_cargar_contenido(a) for a in m.archivos]

    return m


def _cargar_contenido(a: Archivo) -> Archivo:
    '''
    Obtiene los contenidos de los arhivos
    '''
    dir_base = dame(Variable.DIRECTORIO_SISTEMA_ARCHIVOS)

    directorio_absoluto = a.directorio_absoluto(dir_base)
    a.contenido = archivos_util.obtener(directorio_absoluto, a.nombre)

    return a
