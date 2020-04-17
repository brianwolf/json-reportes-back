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
    carpeta_service.crear(carpeta)

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
