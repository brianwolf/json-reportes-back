from typing import List

from apps.models.modelos import Archivo, Modelo
from apps.repositories.models.setup_model import TipoDB, tipo_db_usado


def listado_modelos() -> List[str]:
    '''
    Crea un modelo con sus archivos en la base de datos
    '''
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from apps.repositories.implementations.sqlite.modelo_repository import listado_modelos
    return listado_modelos()


def crear(m: Modelo) -> Modelo:
    '''
    Crea un modelo con sus archivos en la base de datos
    '''
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from apps.repositories.implementations.sqlite.modelo_repository import crear
    return crear(m)


def actualizar(m: Modelo) -> Modelo:
    '''
    Actualiza un modelo en la base de datos
    '''
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from apps.repositories.implementations.sqlite.modelo_repository import actualizar
    return actualizar(m)


def buscar(id: any) -> Modelo:
    '''
    Busca un modelo por id
    '''
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from apps.repositories.implementations.sqlite.modelo_repository import buscar
    return buscar(id)


def buscar_por_filtros(filtros: dict = None) -> List[Modelo]:
    '''
    Busca modelos que cumplan con el filtro
    '''
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from apps.repositories.implementations.sqlite.modelo_repository import buscar_por_filtros
    return buscar_por_filtros(filtros)


def buscar_por_nombre(nombre: str) -> Modelo:
    '''
    Busca un modelo por su nombre
    '''
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from apps.repositories.implementations.sqlite.modelo_repository import buscar_por_nombre
    return buscar_por_nombre(nombre)


def borrar(id: any):
    '''
    Borra un modelo por id
    '''
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from apps.repositories.implementations.sqlite.modelo_repository import borrar
    borrar(id)
