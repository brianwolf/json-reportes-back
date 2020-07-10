import base64
from io import BytesIO

from flask import Blueprint, jsonify, request, send_file

from apps.errors.app_errors import AppException
from apps.errors.conversores_errors import ExtencionesErrors
from apps.errors.modelos_errors import ArchivoErrors, ModelosErrors
from apps.models.conversores import ExtensionArchivo
from apps.models.modelos import Archivo, Modelo, TipoArchivo
from apps.services import modelo_service, reporte_service

blue_print = Blueprint('reportes',
                       __name__,
                       url_prefix='/api/v1/modelos/<nombre_modelo>/reportes')


@blue_print.route('', methods=['GET'])
def listar_todos_los_reportes(nombre_modelo):

    nombres_carpetas = reporte_service.listado_archivos(
        nombre_modelo, TipoArchivo.REPORTE)
    return jsonify(nombres_carpetas), 200


@blue_print.route('/<nombre_reporte>', methods=['GET'])
def obtener(nombre_modelo, nombre_reporte):

    contenidos_tambien = request.args.get('base64') == 'true'

    archivo = reporte_service.obtener_por_nombre(
        nombre_modelo, nombre_reporte, contenidos_tambien=contenidos_tambien)

    return jsonify(archivo.to_json(contenidos_tambien)), 200


@blue_print.route('/<nombre_reporte>/contenido', methods=['GET'])
def obtener_contenido(nombre_modelo, nombre_reporte):

    a = reporte_service.obtener_por_nombre(
        nombre_modelo, nombre_reporte, contenidos_tambien=True)
    if not a:
        mensaje = f'El modelo con nombre {nombre_modelo} no tiene el archivo llamado {nombre_reporte}'
        raise AppException(ArchivoErrors.ARCHIVO_NO_EXISTE, mensaje)

    return send_file(BytesIO(a.contenido),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=nombre_reporte)


@blue_print.route('/<nombre_reporte>/texto', methods=['GET'])
def obtener_contenido_texto_archivo(nombre_modelo, nombre_reporte):

    a = reporte_service.obtener_por_nombre(
        nombre_modelo, nombre_reporte, contenidos_tambien=True)
    if not a:
        mensaje = f'El modelo con nombre {nombre_modelo} no tiene el archivo llamado {nombre_reporte}'
        raise AppException(ArchivoErrors.ARCHIVO_NO_EXISTE, mensaje)

    return a.contenido.decode('utf-8'), 200


@blue_print.route('/<nombre_reporte>/base64', methods=['GET'])
def obtener_contenido_base64_archivo(nombre_modelo, nombre_reporte):

    a = reporte_service.obtener_por_nombre(
        nombre_modelo, nombre_reporte, contenidos_tambien=True)
    if not a:
        mensaje = f'El modelo con nombre {nombre_modelo} no tiene el archivo llamado {nombre_reporte}'
        raise AppException(ArchivoErrors.ARCHIVO_NO_EXISTE, mensaje)

    return a.contenido_base64(), 200


@blue_print.route('/<nombre_reporte>/extension/<extension_reporte>/archivo_origen/<nombre_archivo>/extension/<extension_archivo>', methods=['POST'])
def nuevo_contenido(nombre_modelo, nombre_reporte, extension_reporte, nombre_archivo, extension_archivo):

    m = modelo_service.obtener_por_nombre(nombre_modelo)
    if not m:
        mensaje = f'El modelo con nombre {nombre_modelo} no fue encontrado'
        raise AppException(ModelosErrors.MODELO_NO_EXISTE, mensaje)

    if m.buscar_archivo(nombre_reporte):
        mensaje = f'El nombre {nombre_reporte} ya esta en uso'
        raise AppException(ArchivoErrors.ARCHIVO_YA_EXISTENTE, mensaje)

    a = m.buscar_archivo(nombre_archivo)
    if not a:
        mensaje = f'El archivo con nombre {nombre_archivo} no existe'
        raise AppException(ArchivoErrors.ARCHIVO_NO_EXISTE, mensaje)

    try:
        e_archivo = ExtensionArchivo[str(extension_archivo).upper()]
    except Exception:
        mensaje = f'La extension con nombre {extension_archivo} no es valida'
        raise AppException(ExtencionesErrors.EXTENSION_NO_VALIDA, mensaje)

    try:
        e_reporte = ExtensionArchivo[str(extension_reporte).upper()]
    except Exception:
        mensaje = f'La extension con nombre {extension_reporte} no es valida'
        raise AppException(ExtencionesErrors.EXTENSION_NO_VALIDA, mensaje)

    r = Archivo(nombre_reporte, TipoArchivo.REPORTE)
    r = reporte_service.crear(a, r, request.json, e_archivo, e_reporte)

    return send_file(BytesIO(r.contenido),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=r.nombre)
