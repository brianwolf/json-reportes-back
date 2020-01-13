from io import BytesIO

from flask import Blueprint, Response, jsonify, request, send_file

import apps.configs.variables as var
import apps.services.carpeta_service as carpeta_service
import apps.services.archivo_service as archivo_service
import apps.services.conversor_service as conversor_service
from apps.models.carpeta import TipoCarpeta
from apps.utils.archivos_util import nombre_con_extension

blue_print = Blueprint('reportes', __name__, url_prefix='/api/v1/reportes')


@blue_print.route('/carpeta/<nombre_carpeta>/html/<nombre_html>/pdf/<nombre_pdf>',
                  methods=['POST'])
def html_to_pdf(nombre_carpeta, nombre_html, nombre_pdf):

    json_body = request.json

    nombre_html = nombre_con_extension(nombre_html, 'html')
    nombre_pdf = nombre_con_extension(nombre_pdf, 'pdf')

    modelo = carpeta_service.obtener_por_nombre(nombre_carpeta, True)

    contenido_pdf = conversor_service.html_to_pdf(modelo, json_body, nombre_html,
                                                  nombre_pdf)

    guardar_pdf = request.args.get('guardar') == 'true'
    if not guardar_pdf:
        archivo_service.borrar_contenido_por_tipo(
            TipoCarpeta.PDF, nombre_carpeta, nombre_pdf)

    return send_file(BytesIO(contenido_pdf),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=nombre_pdf)
