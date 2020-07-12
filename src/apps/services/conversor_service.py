import os
from typing import Any
from uuid import uuid4

import pdfkit
from jinja2 import Template

import apps.utils.archivos_util as archivos_util
from apps.configs.variables.lector import Variable, dame
from apps.models.conversores import ExtensionArchivo


def html_a_pdf(html_jinja: bytes, datos: dict) -> bytes:
    '''
    Genera un reporte en pdf aplicando jinja con los datos al archivo html_jinja.
    Devuelve el contenido del archivo generado.
    '''
    nombre_html_temp = f'{uuid4()}.html'
    nombre_pdf_temp = f'{uuid4()}.pdf'
    dir_temp = dame(Variable.DIRECTORIO_TEMP)

    contenido_html = _renderizar_archivo(html_jinja, datos)
    archivos_util.crear(dir_temp, nombre_html_temp, contenido_html)

    ruta_html = os.path.join(dir_temp, nombre_html_temp)
    ruta_pdf = os.path.join(dir_temp, nombre_pdf_temp)

    pdfkit.from_file(ruta_html, ruta_pdf)
    contenido_pdf = archivos_util.obtener(dir_temp, nombre_pdf_temp)

    archivos_util.borrar(dir_temp, nombre_pdf_temp)
    archivos_util.borrar(dir_temp, nombre_html_temp)

    return contenido_pdf


def texto_a_texto(archivo_jinja: bytes, datos: dict) -> bytes:
    '''
    Genera un reporte aplicando jinja con los datos al archivo archivo_jinja.
    Devuelve el contenido del archivo generado
    '''
    return _renderizar_archivo(archivo_jinja, datos)


def _renderizar_archivo(contenido_jinja: bytes, datos: dict) -> bytes:
    str_jinja = contenido_jinja.decode('utf-8')
    template_renderizado = Template(str_jinja).render(datos)
    return bytes(template_renderizado, 'utf-8')


def funcion_conversora(e_origen: ExtensionArchivo, e_destino: ExtensionArchivo) -> Any:
    if e_origen == ExtensionArchivo.HTML and e_destino == ExtensionArchivo.PDF:
        return html_a_pdf

    if e_origen == ExtensionArchivo.MD and e_destino == ExtensionArchivo.MD:
        return texto_a_texto

    return texto_a_texto
