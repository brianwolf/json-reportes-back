from flask import Flask

from apps.configs.lector_variables import _cargar_variables_predefinidas, dame
from apps.configs.rest.blue_prints import carga_dinamica_de_bps
from apps.configs.rest.error_handlers import error_handler_bp
from apps.configs.rest.json import JSONEncoderPersonalizado
from apps.configs.variables.claves import Variable

app = Flask(__name__)
app.register_blueprint(error_handler_bp)
app.json_encoder = JSONEncoderPersonalizado

carga_dinamica_de_bps(app, 'apps/routes')


if __name__ == "__main__":
    flask_host = dame(Variable.PYTHON_HOST)
    flask_port = int(dame(Variable.PYTHON_PORT))

    app.run(host=flask_host, port=flask_port, debug=True)
