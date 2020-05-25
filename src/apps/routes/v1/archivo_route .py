import base64
from enum import Enum
from http import HTTPStatus
from io import BytesIO
from typing import Tuple

from flask import Blueprint, jsonify, request, send_file

import apps.services.archivo_service as archivo_service
from apps.models.errores import AppException
from apps.models.modelos import Archivo, Modelo, TipoArchivo

blue_print = Blueprint('archivos',
                       __name__,
                       url_prefix='/api/v1/modelos/<nombre_modelo>/archivos')


class Errores(Enum):
    ARCHIVO_NO_EXISTE = 'ARCHIVO_NO_EXISTE'


class Errores(Enum):
    ARCHIVO_YA_EXISTENTE = 'ARCHIVO_YA_EXISTENTE'


@blue_print.route('', methods=['GET'])
def listar_todas_los_archivos(nombre_modelo):

    nombres_carpetas = archivo_service.listado_archivos(nombre_modelo)
    return jsonify(nombres_carpetas)


@blue_print.route('/<nombre_archivo>', methods=['GET'])
def obtener_archivo(nombre_modelo, nombre_archivo):

    contenidos_tambien = request.args.get('base64') == 'true'

    archivo = archivo_service.obtener_por_nombre(
        nombre_modelo, nombre_archivo, contenidos_tambien=contenidos_tambien)

    return jsonify(archivo.to_json(contenidos_tambien)), 200


@blue_print.route('/<nombre_archivo>/contenido', methods=['GET'])
def obtener_contenido_archivo(nombre_modelo, nombre_archivo):

    a = archivo_service.obtener_por_nombre(
        nombre_modelo, nombre_archivo, contenidos_tambien=True)
    if not a:
        mensaje = f'El modelo con nombre {nombre_modelo} no tiene el archivo llamado {nombre_archivo}'
        raise AppException(Errores.ARCHIVO_NO_EXISTE, mensaje)

    return send_file(BytesIO(a.contenido),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=nombre_archivo)


@blue_print.route('/<nombre_archivo>/texto', methods=['GET'])
def obtener_contenido_texto_archivo(nombre_modelo, nombre_archivo):

    a = archivo_service.obtener_por_nombre(
        nombre_modelo, nombre_archivo, contenidos_tambien=True)
    if not a:
        mensaje = f'El modelo con nombre {nombre_modelo} no tiene el archivo llamado {nombre_archivo}'
        raise AppException(Errores.ARCHIVO_NO_EXISTE, mensaje)

    return a.contenido.decode('utf-8'), 200


@blue_print.route('/<nombre_archivo>/base64', methods=['GET'])
def obtener_contenido_base64_archivo(nombre_modelo, nombre_archivo):

    a = archivo_service.obtener_por_nombre(
        nombre_modelo, nombre_archivo, contenidos_tambien=True)
    if not a:
        mensaje = f'El modelo con nombre {nombre_modelo} no tiene el archivo llamado {nombre_archivo}'
        raise AppException(Errores.ARCHIVO_NO_EXISTE, mensaje)

    return a.contenido_base64(), 200


# @blue_print.route('/<nombre_archivo>/contenido', methods=['PUT'])
# def reemplazar_contenido_archivo(nombre_modelo, nombre_archivo):

#     archivo_nuevo = Archivo(nombre_archivo, request.get_data())

#     carpeta, _ = _obtener_carpeta_y_archivo(nombre_modelo, nombre_archivo)
#     archivo_service.reemplazar_archivo(carpeta, archivo_nuevo)

#     return ''


# @blue_print.route('/<nombre_archivo>/contenido', methods=['POST'])
# def nuevo_contenido_archivo(nombre_modelo, nombre_archivo):

#     carpeta = carpeta_service.obtener_por_nombre(nombre_modelo, False)
#     archivo = carpeta.buscar_archivo(nombre_archivo)

#     if archivo != None:
#         mensaje = f'El archivo con nombre {nombre_archivo}, ya existe'
#         raise AppException(Errores.ARCHIVO_YA_EXISTENTE, mensaje)

#     archivo_nuevo = Archivo(nombre_archivo, request.get_data())
#     carpeta.agregar_archivo(archivo_nuevo)

#     carpeta_service.actualizar(carpeta)

#     return '', HTTPStatus.CREATED


# @blue_print.route('/<nombre_archivo>/contenido', methods=['DELETE'])
# def borrar_contenido_archivo(nombre_modelo, nombre_archivo):

#     carpeta, archivo = _obtener_carpeta_y_archivo(nombre_modelo,
#                                                   nombre_archivo)

#     archivo_nuevo = Archivo(nombre_archivo, request.get_data())
#     carpeta.borrar_archivo(archivo_nuevo)

#     carpeta_service.actualizar(carpeta)

#     return ''


# def _obtener_contenido(nombre_modelo: str, nombre_archivo: str) -> bytes:
#     '''
#     Obtiene el contenido del archivo
#     '''
#     carpeta, _ = _obtener_carpeta_y_archivo(nombre_modelo, nombre_archivo)

#     return archivo_service.obtener_contenido_por_nombre(
#         carpeta, nombre_archivo)


# def _obtener_carpeta_y_archivo(nombre_modelo: str,
#                                nombre_archivo: str) -> Tuple[Carpeta, Archivo]:
#     '''
#     Obtiene la carpeta y el archivo correspondiente
#     '''
#     carpeta = carpeta_service.obtener_por_nombre(nombre_modelo, False)
#     archivo = carpeta.buscar_archivo(nombre_archivo)

#     if not archivo:
#         mensaje = f'La carpeta {nombre_modelo} no posee el archivo {nombre_archivo}'
#         raise AppException('ARCHIVO_NO_ENCONTRADO', mensaje)

#     return carpeta, archivo
