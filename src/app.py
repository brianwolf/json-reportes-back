from os import path

from flask import Flask

from src.app.configs import variables as variables_proyecto
from src.app.repositories.setup import iniciar_db
from src.libs.logger import logger
from src.libs.rest import rest
from src.libs.variables import variables

variables.iniciar([variables_proyecto])

directorio_logs = variables.dame(variables_proyecto.Variable.DIRECTORIO_LOGS)
nivel_logs = variables.dame(variables_proyecto.Variable.NIVEL_LOGS)
logger.iniciar(directorio_logs, nivel_logs)

app = Flask(__name__)
rest.iniciar(app, 'src/app/routes')

iniciar_db()

if __name__ == "__main__":
    flask_host = variables.dame(variables_proyecto.Variable.PYTHON_HOST)
    flask_port = int(variables.dame(variables_proyecto.Variable.PYTHON_PORT))

    app.run(host=flask_host, port=flask_port, debug=True)
