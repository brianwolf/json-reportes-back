import os
from typing import Any
from uuid import uuid4

import pdfkit
from jinja2 import Template

import apps.utils.archivos_util as archivos_util
from apps.configs.variables.lector import Variable, dame
from apps.models.conversores import ExtensionArchivo, ParametrosCrearReporte
from apps.services import sistema_de_archivos_service as fs


def html_a_pdf(p: ParametrosCrearReporte) -> bytes:
    '''
    Genera un reporte en pdf aplicando jinja con los datos al archivo html_jinja.
    Devuelve el contenido del archivo generado.
    '''
    nombre_html_temp = f'{uuid4()}.html'
    nombre_pdf_temp = f'{uuid4()}.pdf'

    dir_html_temp = fs.obtener_directorio_absoluto(p.a_origen)
    contenido_html = _renderizar_archivo(p.a_origen.contenido, p.datos)

    archivos_util.crear(dir_html_temp, nombre_html_temp, contenido_html)

    ruta_html = os.path.join(dir_html_temp, nombre_html_temp)
    ruta_pdf = os.path.join(dir_html_temp, nombre_pdf_temp)

    pdfkit.from_file(ruta_html, ruta_pdf)
    contenido_pdf = archivos_util.obtener(dir_html_temp, nombre_pdf_temp)

    archivos_util.borrar(dir_html_temp, nombre_pdf_temp)
    archivos_util.borrar(dir_html_temp, nombre_html_temp)

    return contenido_pdf


def texto_a_texto(p: ParametrosCrearReporte) -> bytes:
    '''
    Genera un reporte aplicando jinja con los datos al archivo archivo_jinja.
    Devuelve el contenido del archivo generado
    '''
    return _renderizar_archivo(p.a_origen.contenido, p.datos)


def _renderizar_archivo(contenido_jinja: bytes, datos: dict) -> bytes:
    str_jinja = contenido_jinja.decode('utf-8')
    template_renderizado = Template(str_jinja).render(datos)
    return bytes(template_renderizado, 'utf-8')


def funcion_conversora(parametros: ParametrosCrearReporte) -> Any:
    if parametros.e_origen == ExtensionArchivo.HTML and parametros.e_destino == ExtensionArchivo.PDF:
        return html_a_pdf

    if parametros.e_origen == ExtensionArchivo.MD and parametros.e_destino == ExtensionArchivo.MD:
        return texto_a_texto

    return texto_a_texto
