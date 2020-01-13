from http import HTTPStatus
from io import BytesIO

from flask import Blueprint, jsonify, request, send_file

import apps.configs.variables as var
import apps.services.archivo_service as archivo_service
import apps.services.carpeta_service as carpeta_service
import apps.utils.archivos_util as archivos_util
from apps.configs.loggers import get_logger
from apps.models.carpeta import Archivo, Carpeta, TipoCarpeta
from apps.models.errores import AppException

blue_print = Blueprint('carpetas', __name__, url_prefix='/api/v1/carpetas')


@blue_print.route('', methods=['GET'])
def listar_todas_las_carpetas():

    nombres_carpetas = carpeta_service.listar_todas_las_carpetas()
    return jsonify(nombres_carpetas)


@blue_print.route('/<nombre>', methods=['GET'])
def obtener(nombre):

    contenidos_tambien = request.args.get('base64') == 'true'
    carpeta = carpeta_service.obtener_por_nombre(nombre, contenidos_tambien)

    return jsonify(carpeta.to_dict())


@blue_print.route('/<nombre>', methods=['POST'])
def guardar(nombre):

    archivos = []
    for nombre_archivo, archivo_python in request.files.to_dict().items():

        archivo = Archivo(nombre_archivo, archivo_python.read())
        archivos.append(archivo)

    carpeta = Carpeta(nombre, TipoCarpeta.MODELO, archivos=archivos)
    carpeta_service.guardar(carpeta)

    return '', HTTPStatus.CREATED


@blue_print.route('/<nombre>', methods=['DELETE'])
def borrar(nombre):

    carpeta_service.borrar_por_nombre(nombre)

    return ''


@blue_print.route('/<nombre>', methods=['PUT'])
def reemplazar_por_nombre(nombre):

    borrar(nombre)
    guardar(nombre)

    return ''


@blue_print.route('/<nombre_carpeta>/archivos', methods=['GET'])
def obtener_todos_los_archivos(nombre_carpeta):

    carpeta = carpeta_service.obtener_por_nombre(nombre_carpeta, False)

    archivos_dict = [archivo.to_dict() for archivo in carpeta.archivos]
    return jsonify(archivos_dict)


@blue_print.route('/<nombre_carpeta>/archivos/<nombre_archivo>', methods=['GET'])
def obtener_archivo(nombre_carpeta, nombre_archivo):

    contenidos_tambien = request.args.get('base64') == 'true'

    carpeta = carpeta_service.obtener_por_nombre(nombre_carpeta, False)
    archivo = carpeta.buscar_archivo(nombre_archivo)

    if not archivo:
        mensaje = f'La carpeta {nombre_carpeta} no posee el archivo {nombre_archivo}'
        raise AppException('ARCHIVO_NO_ENCONTRADO', mensaje)

    if contenidos_tambien:
        archivo.contenido = archivo_service.obtener_contenido_por_nombre(
            carpeta, archivo.nombre)

    return jsonify(archivo.to_dict())


@blue_print.route('/<nombre_carpeta>/archivos/<nombre_archivo>/contenido', methods=['GET'])
def obtener_contenido_archivo(nombre_carpeta, nombre_archivo):

    carpeta = carpeta_service.obtener_por_nombre(nombre_carpeta, False)
    archivo = carpeta.buscar_archivo(nombre_archivo)

    if not archivo:
        mensaje = f'La carpeta {nombre_carpeta} no posee el archivo {nombre_archivo}'
        raise AppException('ARCHIVO_NO_ENCONTRADO', mensaje)

    contenido = archivo_service.obtener_contenido_por_nombre(
        carpeta.tipo, carpeta.nombre, archivo.nombre)

    buffer = BytesIO()
    buffer.write(contenido)
    return send_file(BytesIO(contenido),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=nombre_archivo)


@blue_print.route('/<nombre_carpeta>/archivos/<nombre_archivo>/contenido', methods=['PUT'])
def reemplazar_contenido_archivo(nombre_carpeta, nombre_archivo):

    carpeta = carpeta_service.obtener_por_nombre(nombre_carpeta, False)
    archivo = carpeta.buscar_archivo(nombre_archivo)

    if not archivo:
        mensaje = f'La carpeta {nombre_carpeta} no posee el archivo {nombre_archivo}'
        raise AppException('ARCHIVO_NO_ENCONTRADO', mensaje)

    archivo_nuevo = Archivo(nombre_archivo, request.get_data())
    archivo_service.reemplazar_archivo(
        carpeta, archivo_nuevo)

    return ''
