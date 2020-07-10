from typing import List

from apps.models.modelos import Archivo, TipoArchivo
from apps.repositories.setup import _router


def listado_archivos(id_modelo: any, tipo: TipoArchivo = TipoArchivo.MODELO) -> List[str]:
    '''
    Muestra los nombres de los archivos de ese modelo
    '''
    return _router.archivo_repository.listado_archivos(id_modelo, tipo)


def crear(a: Archivo) -> Archivo:
    '''
    Crea un Archivo con sus archivos en la base de datos
    '''
    return _router.archivo_repository.crear(a)


def actualizar(a: Archivo) -> Archivo:
    '''
    Actualiza un Archivo en la base de datos
    '''
    return _router.archivo_repository.actualizar(a)


def buscar(id: any) -> Archivo:
    '''
    Busca un Archivo por id
    '''
    return _router.archivo_repository.buscar(id)


def buscar_por_filtros(filtros: dict = None) -> List[Archivo]:
    '''
    Busca Archivos que cumplan con el filtro
    '''

    return _router.archivo_repository.buscar_por_filtros(filtros)


def borrar(id: any):
    '''
    Borra un Archivo por id
    '''
    _router.archivo_repository.borrar(id)
