from enum import Enum
from io import BytesIO

from flask import Blueprint, Response, jsonify, request, send_file

import apps.services.archivo_service as archivo_service
import apps.services.carpeta_service as carpeta_service
from apps.models.carpeta import TipoCarpeta
from apps.models.errores import AppException

blue_print = Blueprint('archivos', __name__, url_prefix='/api/v1/archivos')


class Errores(Enum):
    TIPO_CARPETA_NO_VALIDO = 'TIPO_CARPETA_NO_VALIDO'
    BORRADO_DE_MODELO_NO_PERMITIDO = 'BORRADO_DE_MODELO_NO_PERMITIDO'


@blue_print.route('/<carpeta_nombre>/<tipo_carpeta_nombre>/<archivo_nombre>', methods=['GET'])
def obtener_archivo(carpeta_nombre: str, tipo_carpeta_nombre: str, archivo_nombre: str):

    tipo_carpeta = TipoCarpeta[tipo_carpeta_nombre.upper()]

    contenido = archivo_service.obtener_contenido_por_tipo_y_nombre(
        tipo_carpeta, carpeta_nombre, archivo_nombre)

    return send_file(BytesIO(contenido),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=archivo_nombre)


@blue_print.route('/<carpeta_nombre>/<tipo_carpeta_nombre>/<archivo_nombre>', methods=['DELETE'])
def borrar_contenido(carpeta_nombre: str, tipo_carpeta_nombre: str, archivo_nombre: str):
    try:
        tipo_carpeta = TipoCarpeta[tipo_carpeta_nombre.upper()]

    except Exception as e:
        mensaje = f'No se reconoce el tipo de carpeta {tipo_carpeta_nombre}'
        raise AppException(Errores.TIPO_CARPETA_NO_VALIDO, mensaje)

    if tipo_carpeta == TipoCarpeta.MODELO:
        mensaje = f'No esta permitido el borrado manual de los archivos del tipo MODELO'
        raise AppException(Errores.BORRADO_DE_MODELO_NO_PERMITIDO, mensaje)

    archivo_service.borrar_contenido_por_tipo(
        tipo_carpeta, carpeta_nombre, archivo_nombre)

    return ''
