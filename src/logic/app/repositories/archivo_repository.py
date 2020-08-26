from typing import List

from logic.app.models.modelos import Archivo, TipoArchivo
from logic.app.repositories.models.setup_model import TipoDB, tipo_db_usado


def listado_archivos(id_modelo: any, tipo: TipoArchivo = TipoArchivo.MODELO) -> List[str]:
    """
    Muestra los nombres de los archivos de ese modelo
    """
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from logic.app.repositories.implementations.sqlite.archivo_repository import listado_archivos
    return listado_archivos(id_modelo, tipo)


def crear(a: Archivo) -> Archivo:
    """
    Crea un Archivo con sus archivos en la base de datos
    """
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from logic.app.repositories.implementations.sqlite.archivo_repository import crear
    return crear(a)


def actualizar(a: Archivo) -> Archivo:
    """
    Actualiza un Archivo en la base de datos
    """
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from logic.app.repositories.implementations.sqlite.archivo_repository import actualizar
    return actualizar(a)


def buscar(id: any) -> Archivo:
    """
    Busca un Archivo por id
    """
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from logic.app.repositories.implementations.sqlite.archivo_repository import buscar
    return buscar(id)


def buscar_por_filtros(filtros: dict = None) -> List[Archivo]:
    """
    Busca Archivos que cumplan con el filtro
    """
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from logic.app.repositories.implementations.sqlite.archivo_repository import buscar_por_filtros
    return buscar_por_filtros(filtros)


def borrar(id: any):
    """
    Borra un Archivo por id
    """
    if tipo_db_usado == TipoDB.MONGODB:
        pass

    from logic.app.repositories.implementations.sqlite.archivo_repository import borrar
    borrar(id)
