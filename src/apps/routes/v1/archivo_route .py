from enum import Enum
from io import BytesIO
from typing import Tuple

from flask import Blueprint, jsonify, request, send_file

import apps.services.archivo_service as archivo_service
import apps.services.carpeta_service as carpeta_service
import apps.utils.archivos_util as archivos_util
from apps.models.carpeta import Archivo, Carpeta, TipoCarpeta
from apps.models.errores import AppException

blue_print = Blueprint('archivos',
                       __name__,
                       url_prefix='/api/v1/carpetas/<nombre_carpeta>/archivos')


class Errores(Enum):
    ARCHIVO_YA_EXISTENTE = 'ARCHIVO_YA_EXISTENTE'


@blue_print.route('', methods=['GET'])
def obtener_todos_los_archivos(nombre_carpeta):

    carpeta = carpeta_service.obtener_por_nombre(nombre_carpeta, False)

    archivos_dict = [archivo.to_dict() for archivo in carpeta.archivos]
    return jsonify(archivos_dict)


@blue_print.route('/<nombre_archivo>', methods=['GET'])
def obtener_archivo(nombre_carpeta, nombre_archivo):

    contenidos_tambien = request.args.get('base64') == 'true'

    carpeta, archivo = _obtener_carpeta_y_archivo(nombre_carpeta,
                                                  nombre_archivo)
    if contenidos_tambien:
        archivo.contenido = archivo_service.obtener_contenido_por_nombre(
            carpeta, nombre_archivo)

    return jsonify(archivo.to_dict())


@blue_print.route('/<nombre_archivo>/contenido', methods=['GET'])
def obtener_contenido_archivo(nombre_carpeta, nombre_archivo):

    contenido = _obtener_contenido(nombre_carpeta, nombre_archivo)
    return send_file(BytesIO(contenido),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=nombre_archivo)


@blue_print.route('/<nombre_archivo>/texto', methods=['GET'])
def obtener_contenido_texto_archivo(nombre_carpeta, nombre_archivo):

    contenido = _obtener_contenido(nombre_carpeta, nombre_archivo)
    return {'contenido': contenido.decode('utf-8')}


@blue_print.route('/<nombre_archivo>/contenido', methods=['PUT'])
def reemplazar_contenido_archivo(nombre_carpeta, nombre_archivo):

    archivo_nuevo = Archivo(nombre_archivo, request.get_data())

    carpeta, _ = _obtener_carpeta_y_archivo(nombre_carpeta, nombre_archivo)
    archivo_service.reemplazar_archivo(carpeta, archivo_nuevo)

    return ''


@blue_print.route('/<nombre_archivo>/contenido', methods=['POST'])
def nuevo_contenido_archivo(nombre_carpeta, nombre_archivo):

    carpeta = carpeta_service.obtener_por_nombre(nombre_carpeta, False)
    archivo = carpeta.buscar_archivo(nombre_archivo)

    if archivo != None:
        mensaje = f'El archivo con nombre {nombre_archivo}, ya existe'
        raise AppException(Errores.ARCHIVO_YA_EXISTENTE, mensaje)

    archivo_nuevo = Archivo(nombre_archivo, request.get_data())
    carpeta.agregar_archivo(archivo_nuevo)

    carpeta_service.actualizar(carpeta)
    archivo_service.guardar_archivo(carpeta, archivo_nuevo)

    return ''


def _obtener_contenido(nombre_carpeta: str, nombre_archivo: str) -> bytes:
    '''
    Obtiene el contenido del archivo
    '''
    carpeta, _ = _obtener_carpeta_y_archivo(nombre_carpeta, nombre_archivo)

    return archivo_service.obtener_contenido_por_nombre(
        carpeta, nombre_archivo)


def _obtener_carpeta_y_archivo(nombre_carpeta: str,
                               nombre_archivo: str) -> Tuple[Carpeta, Archivo]:
    '''
    Obtiene la carpeta y archivos correspondientes
    '''
    carpeta = carpeta_service.obtener_por_nombre(nombre_carpeta, False)
    archivo = carpeta.buscar_archivo(nombre_archivo)

    if not archivo:
        mensaje = f'La carpeta {nombre_carpeta} no posee el archivo {nombre_archivo}'
        raise AppException('ARCHIVO_NO_ENCONTRADO', mensaje)

    return carpeta, archivo
