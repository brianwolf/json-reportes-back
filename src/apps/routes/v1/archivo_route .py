import base64
from enum import Enum
from http import HTTPStatus
from io import BytesIO
from typing import Tuple

from flask import Blueprint, jsonify, request, send_file

from apps.errors.app_errors import AppException
from apps.errors.modelos_errors import ArchivoErrors, ModelosErrors
from apps.models.modelos import Archivo, Modelo, TipoArchivo
from apps.services import archivo_service, modelo_service

blue_print = Blueprint('archivos',
                       __name__,
                       url_prefix='/api/v1/modelos/<nombre_modelo>/archivos')


@blue_print.route('', methods=['GET'])
def listar_todos_los_archivos(nombre_modelo):

    nombres_carpetas = archivo_service.listado_archivos(nombre_modelo)
    return jsonify(nombres_carpetas)


@blue_print.route('/<nombre_archivo>', methods=['GET'])
def obtener(nombre_modelo, nombre_archivo):

    contenidos_tambien = request.args.get('base64') == 'true'

    archivo = archivo_service.obtener_por_nombre(
        nombre_modelo, nombre_archivo, contenidos_tambien=contenidos_tambien)

    return jsonify(archivo.to_json(contenidos_tambien)), 200


@blue_print.route('/<nombre_archivo>/contenido', methods=['GET'])
def obtener_contenido(nombre_modelo, nombre_archivo):

    a = archivo_service.obtener_por_nombre(
        nombre_modelo, nombre_archivo, contenidos_tambien=True)
    if not a:
        mensaje = f'El modelo con nombre {nombre_modelo} no tiene el archivo llamado {nombre_archivo}'
        raise AppException(ArchivoErrors.ARCHIVO_NO_EXISTE, mensaje)

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
        raise AppException(ArchivoErrors.ARCHIVO_NO_EXISTE, mensaje)

    return a.contenido.decode('utf-8'), 200


@blue_print.route('/<nombre_archivo>/base64', methods=['GET'])
def obtener_contenido_base64_archivo(nombre_modelo, nombre_archivo):

    a = archivo_service.obtener_por_nombre(
        nombre_modelo, nombre_archivo, contenidos_tambien=True)
    if not a:
        mensaje = f'El modelo con nombre {nombre_modelo} no tiene el archivo llamado {nombre_archivo}'
        raise AppException(ArchivoErrors.ARCHIVO_NO_EXISTE, mensaje)

    return a.contenido_base64(), 200


@blue_print.route('/<nombre_archivo>/contenido', methods=['PUT'])
def actualizar_contenido(nombre_modelo, nombre_archivo):

    a = archivo_service.obtener_por_nombre(nombre_modelo, nombre_archivo)
    if not a:
        mensaje = f'El archivo con nombre {nombre_archivo} y modelo llamado {nombre_modelo} no fue encontrado'
        raise AppException(ArchivoErrors.ARCHIVO_NO_EXISTE, mensaje)

    a.contenido = request.data
    archivo_service.actualizar_contenido(a)

    return '', 200


@blue_print.route('/<nombre_archivo>/contenido', methods=['POST'])
def nuevo_contenido(nombre_modelo, nombre_archivo):

    m = modelo_service.obtener_por_nombre(nombre_modelo)

    if not m:
        mensaje = f'El modelo con nombre {nombre_modelo} no fue encontrado'
        raise AppException(ModelosErrors.MODELO_NO_EXISTE, mensaje)

    if m.buscar_archivo(nombre_archivo):
        mensaje = f'El nombre {nombre_modelo} ya esta en uso'
        raise AppException(ArchivoErrors.ARCHIVO_YA_EXISTENTE, mensaje)

    a = Archivo(nombre_archivo, m.directorio_relativo(
        TipoArchivo.MODELO), TipoArchivo.MODELO)
    a.contenido = request.data
    a.id_modelo = m.id

    archivo_service.crear(a)

    return '', 200
