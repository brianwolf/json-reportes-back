from http import HTTPStatus

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException

from apps.configs.loggers import get_logger
from apps.models.errores import AppException

__version__ = '1.0.1'

error_handler_bp = Blueprint('handlers', __name__)

logger = get_logger()


@error_handler_bp.app_errorhandler(HTTPException)
def handle_exception(httpe):
    return '', httpe.code


@error_handler_bp.app_errorhandler(Exception)
def handle_exception(e):
    logger.exception(e)
    return '', HTTPStatus.INTERNAL_SERVER_ERROR


@error_handler_bp.app_errorhandler(AppException)
def handle_business_exception(ae: AppException):
    logger.warning(ae.to_dict())
    return ae.respuesta_json()
