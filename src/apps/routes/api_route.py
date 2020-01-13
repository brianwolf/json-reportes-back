from flask import Blueprint, jsonify, request

import apps.configs.variables as var
from apps.configs.loggers import get_logger
from apps.models.errores import AppException

blue_print = Blueprint('base', __name__, url_prefix='')

logger = get_logger()


@blue_print.route('/variables')
def variables():
    respuesta = {}
    for key in var.mapa_variables.keys():
        respuesta[key] = var.get(key)

    return jsonify(respuesta)


@blue_print.route('/errores')
def error():
    raise AppException('PRUEBA', 'Rompimos todo vieja!')


@blue_print.route('/')
def vivo():
    logger.info("VIVO")
    respuesta = {"estado": "vivo"}
    return jsonify(respuesta)
