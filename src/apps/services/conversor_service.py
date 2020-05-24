import os
from uuid import uuid4

import pdfkit
from jinja2 import Template

import apps.utils.archivos_util as archivos_util
from apps.configs.logger.logger import obtener_logger
from apps.configs.variables.claves import Variable
from apps.configs.variables.lector import dame


def html_a_pdf(html_jinja: str, datos: dict) -> bytes:
    '''
    Genera un reporte en pdf aplicando jinja con los datos al archivo html_jinja.
    Devuelve el contenido del archivo generado.
    '''
    nombre_html_temp = f'{uuid4()}.html'
    nombre_pdf_temp = f'{uuid4()}.pdf'
    dir_temp = dame(Variable.DIRECTORIO_TEMP)

    contenido_html = _renderizar_archivo(html_jinja, datos)
    archivos_util.crear(dir_temp, nombre_html_temp, contenido_html)

    ruta_html = os.path(dir_temp, nombre_html_temp)
    ruta_pdf = os.path(dir_temp, nombre_pdf_temp)

    pdfkit.from_file(ruta_html, ruta_pdf)
    contenido_pdf = archivos_util.obtener(dir_temp, nombre_pdf_temp)

    archivos_util.borrar(dir_temp, nombre_pdf_temp)
    archivos_util.borrar(dir_temp, nombre_html_temp)

    return contenido_pdf


def texto_a_texto(archivo_jinja: str, datos: dict) -> bytes:
    '''
    Genera un reporte aplicando jinja con los datos al archivo archivo_jinja.
    Devuelve el contenido del archivo generado
    '''
    return _renderizar_archivo(archivo_jinja, datos)


def _renderizar_archivo(contenido_jinja: str, datos: dict) -> bytes:

    template_renderizado = Template(contenido_jinja).render(datos)
    return bytes(template_renderizado, 'utf-8')
