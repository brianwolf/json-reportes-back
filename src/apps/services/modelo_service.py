from enum import Enum
from typing import List

from apps.configs.variables.lector import Variable, dame
from apps.models.errores import AppException
from apps.models.modelos import Archivo, Modelo
from apps.repositories import modelo_repository
from apps.services import archivo_service


class Errores(Enum):
    NOMBRE_EN_USO = 'NOMBRE_EN_USO'
    MODELO_NO_EXISTE = 'MODELO_NO_EXISTE'


def listado_modelos() -> List[str]:
    '''
    Devuelve una lista con los nombres de todas las modelos en la app
    '''
    return modelo_repository.listado_modelos()


def crear(m: Modelo) -> Modelo:
    '''
    Crea un modelo en la base de datos y en el sistema de archivos,
    devuelve el id del modelo y los ids de los archivos generados
    '''
    if modelo_repository.buscar_por_nombre(m.nombre):
        mensaje = f'El nombre {m.nombre} ya esta en uso'
        raise AppException(Errores.NOMBRE_EN_USO, mensaje)

    m = modelo_repository.crear(m)

    archivos_insertados = []
    for a in m.archivos:
        a.id_modelo = m.id
        archivos_insertados.append(archivo_service.crear(a))

    m.archivos = archivos_insertados
    return m


def actualizar(m: Modelo) -> Modelo:
    '''
    Actualiza una modelo en la base de datos y en el sistema de archivos
    '''
    m_viejo = obtener(m.id)
    if not m_viejo:
        mensaje = f'El modelo con id {m.id} no fue encontrado'
        raise AppException(Errores.MODELO_NO_EXISTE, mensaje)

    archivos_a_borrar = [
        archivo for archivo in m_viejo.archivos
        if archivo not in m.archivos
    ]
    archivos_a_crear = [
        archivo for archivo in m.archivos
        if archivo not in m_viejo.archivos
    ]

    m = modelo_repository.actualizar(m)

    for a in archivos_a_borrar:
        archivo_service.borrar(a)

    archivos_nuevos = []
    for archivo in archivos_a_crear:
        archivos_nuevos.append(archivo_service.crear(a))

    m.archivos = archivos_nuevos
    return m


def borrar_por_nombre(nombre: str):
    """
    Borra una modelo en la base de datos y en el sistema de archivos buscando por nombre
    """
    m = modelo_repository.buscar_por_nombre(nombre)
    if not m:
        mensaje = f'El modelo con nombre {nombre} no fue encontrado'
        raise AppException(Errores.MODELO_NO_EXISTE, mensaje)

    modelo_repository.borrar(m.id)

    for a in m.archivos:
        archivo_service.borrar(a)


def obtener_por_nombre(nombre: str, contenidos_tambien: bool = False) -> Modelo:
    '''
    Obtiene una modelo de la base de datos y del sistema de archivos
    '''
    m = modelo_repository.buscar_por_nombre(nombre)

    if contenidos_tambien:
        for a in m.archivos:
            a.contenido = archivo_service.obtener_contenido(a)

    return m


def obtener(id: int, contenidos_tambien: bool = False) -> Modelo:
    '''
    Obtiene una modelo de la base de datos y del sistema de archivos
    '''
    m = modelo_repository.buscar(id)

    if contenidos_tambien:
        for a in m.archivos:
            a.contenido = archivo_service.obtener_contenido(a)

    return m
