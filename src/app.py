from flask import Flask

from apps.configs.error_handlers import error_handler_bp
from apps.configs.flask import CustomJSONEncoder
from apps.configs.lector_variables import dame
from apps.configs.variables import Variable
from apps.utils.carga_dinamica_blue_prints import registrar_blue_prints

_PYTHON_HOST = dame(Variable.PYTHON_HOST)
_PYTHON_PORT = int(dame(Variable.PYTHON_PORT))

app = Flask(__name__)
app.register_blueprint(error_handler_bp)
app.json_encoder = CustomJSONEncoder

registrar_blue_prints(app, 'apps/routes')

if __name__ == "__main__":
    app.run(host=_PYTHON_HOST, port=_PYTHON_PORT, debug=True)
