from typing import List

from logic.app.models.conversores import ParametrosCrearReporte
from logic.app.models.modelos import Archivo, TipoArchivo
from logic.app.services import archivo_service, conversor_service


def listado_reportes(nombre_modelo: str) -> List[str]:
    """
    Devuelve una lista con los nombres de todos los archivos de un modelo en la app
    """
    return archivo_service.listado_archivos(nombre_modelo, TipoArchivo.REPORTE)


def crear(p: ParametrosCrearReporte) -> Archivo:
    """
    Genera un reporte y lo guarda en la base de datos y en el sistema de archivos
    """
    if not p.a_origen.contenido:
        p.a_origen.contenido = archivo_service.obtener_contenido(p.a_origen)

    funcion_conversora = conversor_service.funcion_conversora(p)

    p.a_destino.contenido = funcion_conversora(p)
    p.a_destino.tipo = TipoArchivo.REPORTE
    p.a_destino.id_modelo = p.a_origen.id_modelo

    reporte = archivo_service.crear(p.a_destino)
    if not p.guardar:
        archivo_service.borrar(reporte.id)
        reporte.id = None
        reporte.uuid_guardado = None

    return reporte


def borrar(id_reporte: any):
    """
    Borra un reporte en la base de datos y en el sistema de archivos buscando por nombre
    """
    archivo_service.borrar(id_reporte)


def obtener_por_nombre(nombre_modelo: str, nombre_reporte: str, contenidos_tambien: bool = False) -> Archivo:
    """
    Obtiene un reporte de la base de datos y del sistema de archivos
    """
    return archivo_service.obtener_por_nombre(nombre_modelo, nombre_reporte, contenidos_tambien)


def obtener(id_reporte: int, contenidos_tambien: bool = False) -> Archivo:
    """
    Obtiene un reporte de la base de datos y del sistema de archivos
    """
    return archivo_service.obtener(id_reporte, contenidos_tambien)


def obtener_contenido(id_reporte: int, contenidos_tambien: bool = False) -> bytes:
    """
    Obtiene el contenido del reporte
    """
    return archivo_service.obtener(id_reporte, contenidos_tambien).contenido


def actualizar_contenido(r: Archivo):
    """
    Actualiza el contenido de un reporte
    """
    archivo_service.actualizar_contenido(r)
