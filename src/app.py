from flask import Flask

import apps.configs.variables as var
from apps.configs.error_handlers import error_handler_bp
from apps.utils.flask_util import registrar_blue_prints

PYTHON_HOST = var.get('PYTHON_HOST')
PYTHON_PORT = int(var.get('PYTHON_PORT'))

app = Flask(__name__)
app.register_blueprint(error_handler_bp)

registrar_blue_prints(app, 'apps/routes')

if __name__ == "__main__":
    app.run(host=PYTHON_HOST, port=PYTHON_PORT, debug=True)
