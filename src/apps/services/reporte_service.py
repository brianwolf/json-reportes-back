from typing import List

from apps.models.conversores import ExtensionArchivo
from apps.models.modelos import Archivo, TipoArchivo
from apps.services import archivo_service, conversor_service


def listado_reportes(nombre_modelo: str) -> List[str]:
    '''
    Devuelve una lista con los nombres de todos los archivos de un modelo en la app
    '''
    return archivo_service.listado_archivos(nombre_modelo, TipoArchivo.REPORTE)


def crear(a_origen: Archivo, a_destino: Archivo, datos: dict, e_origen: ExtensionArchivo, e_destino: ExtensionArchivo, guardar: bool = True) -> Archivo:
    '''
    Genera un reporte y lo guarda en la base de datos y en el sistema de archivos
    '''
    if not a_origen.contenido:
        a_origen.contenido = archivo_service.obtener_contenido(a_origen)

    funcion_conversora = conversor_service.funcion_conversora(
        e_origen, e_destino)

    a_destino.contenido = funcion_conversora(a_origen.contenido, datos)
    a_destino.tipo = TipoArchivo.REPORTE
    a_destino.id_modelo = a_origen.id_modelo

    reporte = archivo_service.crear(a_destino)
    if not guardar:
        archivo_service.borrar(reporte.id)
        reporte.id = None
        reporte.uuid_guardado = None

    return reporte


def borrar(id: any):
    """
    Borra un reporte en la base de datos y en el sistema de archivos buscando por nombre
    """
    archivo_service.borrar(id)


def obtener_por_nombre(nombre_modelo: str, nombre_reporte: str, contenidos_tambien: bool = False) -> Archivo:
    '''
    Obtiene un reporte de la base de datos y del sistema de archivos
    '''
    return archivo_service.obtener_por_nombre(nombre_modelo, nombre_reporte, contenidos_tambien)


def obtener(id: int, contenidos_tambien: bool = False) -> Archivo:
    '''
    Obtiene un reporte de la base de datos y del sistema de archivos
    '''
    return archivo_service.obtener(id, contenidos_tambien)


def obtener_contenido(r: Archivo) -> bytes:
    '''
    Obtiene el contenido del reporte
    '''
    return archivo_service.obtener(r)


def actualizar_contenido(r: Archivo):
    '''
    Actualiza el contenido de un reporte
    '''
    archivo_service.actualizar_contenido(r)
