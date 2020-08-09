from flask import Flask

from apps.configs.rest.blue_prints import carga_dinamica_de_bps
from apps.configs.rest.error_handlers import error_handler_bp
from apps.configs.rest.json import JSONEncoderPersonalizado


def config(app: Flask, directorio_rutas: str):
    '''
    Configura el logger para el proyecto
    '''
    app.register_blueprint(error_handler_bp)
    app.json_encoder = JSONEncoderPersonalizado

    carga_dinamica_de_bps(app, directorio_rutas)
