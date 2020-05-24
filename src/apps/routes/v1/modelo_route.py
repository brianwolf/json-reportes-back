from io import BytesIO

from flask import Blueprint, jsonify, request, send_file

import apps.configs.variables as var
import apps.services.modelo_service as modelo_service
from apps.configs.logger.logger import obtener_logger
from apps.models.errores import AppException
from apps.models.modelos import Archivo, Modelo, TipoArchivo
from apps.services import reporte_service

blue_print = Blueprint('modelos', __name__, url_prefix='/api/v1/modelos')


@blue_print.route('', methods=['GET'])
def listar_todas_las_carpetas():

    nombres_carpetas = modelo_service.listado_modelos()
    return jsonify(nombres_carpetas)


@blue_print.route('/<nombre>', methods=['GET'])
def obtener(nombre):

    contenidos_tambien = request.args.get('base64') == 'true'
    modelo = modelo_service.obtener_por_nombre(nombre, contenidos_tambien)
    return jsonify(modelo.to_json()), 200


@blue_print.route('/<nombre>', methods=['POST'])
def guardar(nombre):

    descripcion = request.args.get('descripcion')

    m = Modelo(nombre, descripcion)

    archivos = []
    for nombre, archivo_python in request.files.to_dict().items():
        dir_relativo = m.directorio_relativo(TipoArchivo.MODELO)
        archivos.append(Archivo(nombre, dir_relativo,
                                TipoArchivo.MODELO, archivo_python.read()))

    m.archivos = archivos
    modelo_service.crear(m)
    return jsonify(m.to_json()), 201


@blue_print.route('/<nombre>', methods=['DELETE'])
def borrar(nombre):

    modelo_service.borrar_por_nombre(nombre)
    return '', 200


@blue_print.route('/<nombre>', methods=['PUT'])
def reemplazar_por_nombre(nombre):

    borrar(nombre)
    guardar(nombre)
    return '', 200
