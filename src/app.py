from os import path

from flask import Flask

from logic.app.configs import variables as variables_proyecto
from logic.app.repositories.setup import iniciar_db
from logic.libs.logger import logger
from logic.libs.rest import rest
from logic.libs.variables import variables

variables.iniciar([variables_proyecto])

directorio_logs = variables.dame(variables_proyecto.Variable.DIRECTORIO_LOGS)
nivel_logs = variables.dame(variables_proyecto.Variable.NIVEL_LOGS)
logger.iniciar(directorio_logs, nivel_logs)

app = Flask(__name__)
rest.iniciar(app, 'logic/app/routes')

iniciar_db()

if __name__ == "__main__":
    flask_host = variables.dame(variables_proyecto.Variable.PYTHON_HOST)
    flask_port = int(variables.dame(variables_proyecto.Variable.PYTHON_PORT))

    app.run(host=flask_host, port=flask_port, debug=True)
