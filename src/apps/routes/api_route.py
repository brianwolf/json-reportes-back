from flask import Blueprint, jsonify, render_template

from apps.configs.lector_variables import variables_cargadas
from apps.configs.loggers import get_logger

blue_print = Blueprint('api', __name__, url_prefix='',
                       template_folder='resources/web/', static_folder='resources/web/')

logger = get_logger()


@blue_print.route('/variables')
def variables():
    return jsonify(variables_cargadas())


@blue_print.route('/vivo')
def vivo():
    logger.info("VIVO")
    return jsonify({"estado": "vivo"})


@blue_print.route('/')
def index():
    return render_template("index.html")
