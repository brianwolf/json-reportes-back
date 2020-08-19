from typing import List

from apps.models.modelos import Archivo, Modelo
from apps.repositories.setup import _router


def listado_modelos() -> List[str]:
    '''
    Crea un modelo con sus archivos en la base de datos
    '''
    return _router.modelo_repository.listado_modelos()


def crear(m: Modelo) -> Modelo:
    '''
    Crea un modelo con sus archivos en la base de datos
    '''
    return _router.modelo_repository.crear(m)


def actualizar(m: Modelo) -> Modelo:
    '''
    Actualiza un modelo en la base de datos
    '''
    return _router.modelo_repository.actualizar(m)


def buscar(id: any) -> Modelo:
    '''
    Busca un modelo por id
    '''
    return _router.modelo_repository.buscar(id)


def buscar_por_filtros(filtros: dict = None) -> List[Modelo]:
    '''
    Busca modelos que cumplan con el filtro
    '''
    return _router.modelo_repository.buscar_por_filtros(filtros)


def buscar_por_nombre(nombre: str) -> Modelo:
    '''
    Busca un modelo por su nombre
    '''
    return _router.modelo_repository.buscar_por_nombre(nombre)


def borrar(id: any):
    '''
    Borra un modelo por id
    '''
    _router.modelo_repository.borrar(id)
