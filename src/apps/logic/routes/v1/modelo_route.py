from io import BytesIO

from flask import Blueprint, jsonify, request, send_file

import apps.logic.services.modelo_service as modelo_service
from apps.libs.excepcion.excepcion import AppException
from apps.logic.models.modelos import Archivo, Modelo, TipoArchivo
from apps.logic.services import reporte_service

blue_print = Blueprint('modelos', __name__, url_prefix='/api/v1/modelos')


@blue_print.route('', methods=['GET'])
def listar_todas_las_carpetas():

    nombres_carpetas = modelo_service.listado_modelos()
    return jsonify(nombres_carpetas)


@blue_print.route('/<nombre>', methods=['GET'])
def obtener(nombre):

    contenidos_tambien = request.args.get('base64') == 'true'
    modelo = modelo_service.obtener_por_nombre(nombre, contenidos_tambien)
    if not modelo:
        return '', 204

    return jsonify(modelo.to_json(contenidos_tambien)), 200


@blue_print.route('/<nombre>', methods=['POST'])
def guardar(nombre):

    descripcion = request.args.get('descripcion')

    m = Modelo(nombre, descripcion)

    archivos = []
    for nombre, archivo_python in request.files.to_dict().items():
        archivos.append(
            Archivo(nombre, TipoArchivo.MODELO, archivo_python.read()))

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
