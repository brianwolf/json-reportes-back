from flask import Blueprint, jsonify, request

from apps.configs.lector_variables import variables_cargadas
from apps.configs.loggers import get_logger
from apps.models.errores import AppException

blue_print = Blueprint('api', __name__, url_prefix='')

logger = get_logger()


@blue_print.route('/variables')
def variables():
    return jsonify(variables_cargadas())


@blue_print.route('/vivo')
def vivo():
    logger.info("VIVO")
    return jsonify({"estado": "vivo"})
