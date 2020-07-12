from http import HTTPStatus

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException

from apps.configs.logger.logger import obtener_logger
from apps.errors.app_errors import AppException, UnknownException

__version__ = '1.1.0'

error_handler_bp = Blueprint('handlers', __name__)

_logger = obtener_logger()


@error_handler_bp.app_errorhandler(HTTPException)
def handle_exception(httpe):
    return '', httpe.code


@error_handler_bp.app_errorhandler(Exception)
def handle_exception(e: Exception):
    _logger.exception(e)
    return UnknownException(e).respuesta_json()


@error_handler_bp.app_errorhandler(AppException)
def handle_business_exception(ae: AppException):
    _logger.warning(ae.to_json())
    return ae.respuesta_json()
