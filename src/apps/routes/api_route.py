from flask import Blueprint, jsonify, render_template

from apps.configs.logger.logger import obtener_logger
from apps.configs.variables.lector import variables_cargadas

blue_print = Blueprint('api', __name__, url_prefix='',
                       template_folder='consume/static/web/', static_folder='consume/static/web/')

_logger = obtener_logger()


@blue_print.route('/variables')
def variables():
    return jsonify(variables_cargadas())


@blue_print.route('/vivo')
def vivo():
    _logger.info("VIVO")
    return jsonify({"estado": "vivo"})


@blue_print.route('/')
def index():
    return render_template("index.html")
