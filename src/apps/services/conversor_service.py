import os
import uuid
from enum import Enum

import pdfkit
from jinja2 import Template

import apps.configs.variables as var
import apps.services.archivo_service as archivo_service
import apps.utils.archivos_util as archivos_util
from apps.configs.loggers import get_logger
from apps.models.carpeta import Archivo, Carpeta, TipoCarpeta
from apps.models.errores import AppException


class Errores(Enum):
    ARCHIVO_NO_EXISTE = 'ARCHIVO_NO_EXISTE'


def html_to_pdf(carpeta: Carpeta, datos: dict, nombre_html: str,
                nombre_pdf: str) -> bytes:
    '''
    Genera un reporte en pdf aplicando los datos al modelo
    Devuelve la ruta interna de donde guardo el archivo
    '''
    html = carpeta.buscar_archivo(nombre_html)
    if html is None:
        mensaje = f'El archivo {nombre_html} no existe'
        raise AppException(Errores.ARCHIVO_NO_EXISTE, mensaje)

    html_renderizado = _renderizar_archivo(html, datos)

    archivo_service.guardar_archivo(carpeta, html_renderizado)

    directorio_pdf = archivos_util.ruta_tipo_carpeta(TipoCarpeta.PDF.value,
                                                     carpeta.nombre)
    archivos_util.crear_directorio_si_no_existe(directorio_pdf)

    ruta_pdf = directorio_pdf + nombre_pdf
    ruta_html = archivos_util.ruta_archivo(carpeta.tipo.value, carpeta.nombre,
                                           html_renderizado.nombre)

    pdfkit.from_file(ruta_html, ruta_pdf)

    archivo_service.borrar_contenido(carpeta, html_renderizado.nombre)

    return archivos_util.obtener_archivo(directorio_pdf + nombre_pdf)


def _renderizar_archivo(archivo: Archivo, datos: dict) -> Archivo:

    template_renderizado = Template(archivo.contenido_str()).render(datos)

    nombre = str(uuid.uuid4()) + '.html'
    contenido = bytes(template_renderizado, 'utf-8')

    html_temporal = Archivo(nombre, contenido)

    return html_temporal
