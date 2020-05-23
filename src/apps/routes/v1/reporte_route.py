from enum import Enum
from io import BytesIO

from flask import Blueprint, request, send_file

import apps.services.archivo_service as archivo_service
import apps.services.carpeta_service as carpeta_service
import apps.services.conversor_service as conversor_service
from apps.models.carpeta import TipoCarpeta
from apps.models.errores import AppException
from apps.utils.archivos_util import nombre_con_extension

blue_print = Blueprint('reportes', __name__, url_prefix='/api/v1/reportes')


class Errores(Enum):
    CARPETA_NO_EXISTE = 'CARPETA_NO_EXISTE'
    TIPO_CARPETA_NO_VALIDO = 'TIPO_CARPETA_NO_VALIDO'
    BORRADO_DE_MODELO_NO_PERMITIDO = 'BORRADO_DE_MODELO_NO_PERMITIDO'


@blue_print.route('/carpeta/<carpeta_nombre>/<tipo_carpeta_nombre>/<archivo_nombre>',
                  methods=['GET'])
def obtener_archivo(carpeta_nombre: str, tipo_carpeta_nombre: str, archivo_nombre: str):
    try:
        tipo_carpeta = TipoCarpeta.desde_str(tipo_carpeta_nombre)

    except Exception:
        mensaje = f'No se reconoce el tipo de carpeta {tipo_carpeta_nombre}'
        raise AppException(Errores.TIPO_CARPETA_NO_VALIDO, mensaje)

    carpeta_existe = carpeta_service.obtener_por_nombre(carpeta_nombre, False)
    if not carpeta_existe:
        mensaje = f'La carpeta {carpeta_nombre} NO existe'
        raise AppException(Errores.CARPETA_NO_EXISTE, mensaje)

    contenido = archivo_service.obtener_contenido_por_tipo_y_nombre(
        tipo_carpeta, carpeta_nombre, archivo_nombre)

    return send_file(BytesIO(contenido),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=archivo_nombre)


@blue_print.route('/carpeta/<carpeta_nombre>/<tipo_carpeta_nombre>/<archivo_nombre>',
                  methods=['DELETE'])
def borrar_contenido(carpeta_nombre: str, tipo_carpeta_nombre: str, archivo_nombre: str):
    try:
        tipo_carpeta = TipoCarpeta.desde_str(tipo_carpeta_nombre)

    except Exception:
        mensaje = f'No se reconoce el tipo de carpeta {tipo_carpeta_nombre}'
        raise AppException(Errores.TIPO_CARPETA_NO_VALIDO, mensaje)

    if tipo_carpeta == TipoCarpeta.MODELO:
        mensaje = f'No esta permitido el borrado manual de los archivos del tipo MODELO'
        raise AppException(Errores.BORRADO_DE_MODELO_NO_PERMITIDO, mensaje)

    carpeta_existe = carpeta_service.obtener_por_nombre(carpeta_nombre, False)
    if not carpeta_existe:
        mensaje = f'La carpeta {carpeta_nombre} NO existe'
        raise AppException(Errores.CARPETA_NO_EXISTE, mensaje)

    archivo_service.borrar_contenido_por_tipo(tipo_carpeta, carpeta_nombre,
                                              archivo_nombre)
    return ''


@blue_print.route(
    '/carpeta/<nombre_carpeta>/html/<nombre_html>/pdf/<nombre_pdf>',
    methods=['POST'])
def html_a_pdf(nombre_carpeta, nombre_html, nombre_pdf):

    json_body = request.json

    nombre_html = nombre_con_extension(nombre_html, 'html')
    nombre_pdf = nombre_con_extension(nombre_pdf, 'pdf')

    modelo = carpeta_service.obtener_por_nombre(nombre_carpeta, True)

    contenido_pdf = conversor_service.html_a_pdf(modelo, json_body,
                                                 nombre_html, nombre_pdf)

    guardar_pdf = request.args.get('guardar') == 'true'
    if not guardar_pdf:
        archivo_service.borrar_contenido_por_tipo(TipoCarpeta.PDF,
                                                  nombre_carpeta, nombre_pdf)

    return send_file(BytesIO(contenido_pdf),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=nombre_pdf)


@blue_print.route(
    '/carpeta/<nombre_carpeta>/md/<nombre_entrada>/md/<nombre_salida>',
    methods=['POST'])
def md_a_md(nombre_carpeta, nombre_entrada, nombre_salida):

    json_body = request.json

    nombre_entrada = nombre_con_extension(nombre_entrada, 'md')
    nombre_salida = nombre_con_extension(nombre_salida, 'md')

    carpeta = carpeta_service.obtener_por_nombre(nombre_carpeta, True)

    contenido_resultado = conversor_service.texto_a_texto(carpeta, json_body,
                                                          nombre_entrada, nombre_salida)

    guardar_resultado = request.args.get('guardar') == 'true'
    if not guardar_resultado:
        archivo_service.borrar_contenido_por_tipo(TipoCarpeta.MD,
                                                  nombre_carpeta, nombre_salida)

    return send_file(BytesIO(contenido_resultado),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=nombre_salida)
