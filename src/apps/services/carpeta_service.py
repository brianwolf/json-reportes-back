from uuid import UUID

import apps.configs.variables as var
import apps.repositories.carpeta_repository as carpeta_repository
import apps.services.archivo_service as archivo_service
import apps.utils.archivos_util as archivos_util
from apps.configs.loggers import get_logger
from apps.models.carpeta import Archivo, Carpeta, TipoCarpeta
from apps.models.errores import AppException


def listar_todas_las_carpetas() -> list:
    '''
    Devuelve una lista con los nombres de todas las carpetas en la app
    '''
    return archivos_util.listado_archivos_directorio_base()


def guardar(carpeta: Carpeta) -> UUID:
    '''
    Guarda un modelo en la base de datos y en el sistema de archivos
    '''
    id_generada = carpeta_repository.guardar(carpeta)
    try:
        for archivo in carpeta.archivos:
            archivo_service.guardar_archivo(carpeta, archivo)

    except AppException as ae:
        archivo_service.borrar_carpeta_y_archivos(carpeta.tipo, carpeta.nombre)
        carpeta_repository.borrar(carpeta)
        raise ae

    return id_generada


def actualizar(carpeta: Carpeta) -> None:
    '''
    Actualiza una carpeta en la base de datos y en el sistema de archivos
    '''
    carpeta_vieja = obtener(carpeta.nombre)

    archivos_a_borrar = [
        archivo for archivo in carpeta_vieja.archivos
        if archivo not in carpeta.archivos
    ]
    archivos_a_crear = [
        archivo for archivo in carpeta.archivos
        if archivo not in carpeta_vieja.archivos
    ]

    carpeta_repository.actualizar(carpeta)

    for archivo in archivos_a_borrar:
        archivo_service.borrar_contenido(carpeta, archivo.nombre)

    for archivo in archivos_a_crear:
        archivo_service.guardar_archivo(carpeta, archivo)

    return id_generada


def borrar_por_nombre(nombre: str):
    """
    Borra una carpeta en la base de datos y en el sistema de archivos buscando por nombre
    """
    carpeta = carpeta_repository.buscar_por_nombre(nombre)
    carpeta_repository.borrar(carpeta)

    archivo_service.borrar_carpeta_y_archivos(carpeta)


def obtener_por_nombre(nombre: str,
                       contenidos_tambien: bool = False) -> Carpeta:
    '''
    Obtiene una carpeta de la base de datos y del sistema de archivos
    '''
    carpeta = carpeta_repository.buscar_por_nombre(nombre)
    carpeta.archivos = _obtener_archivos(carpeta, contenidos_tambien)

    return carpeta


def obtener(id: UUID,
            contenidos_tambien: bool = False) -> Carpeta:
    '''
    Obtiene una carpeta de la base de datos y del sistema de archivos
    '''
    carpeta = carpeta_repository.buscar(id)
    carpeta.archivos = _obtener_archivos(carpeta, contenidos_tambien)

    return carpeta


def _obtener_archivos(carpeta: Carpeta,
                      contenidos_tambien: bool = False) -> list:
    '''
    Obtiene los archivos de una carpeta
    '''
    archivos = []
    for archivo in carpeta.archivos:

        if contenidos_tambien:
            contenido = archivo_service.obtener_contenido_por_nombre(
                carpeta, archivo.nombre)

            archivo.contenido = contenido

        archivos.append(archivo)

    return archivos
