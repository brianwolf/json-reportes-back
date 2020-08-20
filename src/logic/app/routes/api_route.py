from flask import Blueprint, jsonify, render_template

from logic.libs.logger.logger import log
from logic.libs.variables.variables import variables_cargadas

blue_print = Blueprint('api', __name__, url_prefix='',
                       template_folder='consume/static/web/', static_folder='consume/static/web/')


@blue_print.route('/variables')
def variables():
    return jsonify(variables_cargadas())


@blue_print.route('/vivo')
def vivo():
    log().info("VIVO")
    return jsonify({"estado": "vivo"})


@blue_print.route('/')
def index():
    return render_template("index.html")
