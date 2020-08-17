from os import path

from flask import Flask

from apps.config import claves
from apps.repositories.setup import iniciar_db
from apps.utils.rest.init import init as rest_init
from apps.utils.variables.init import init as vars_init
from apps.utils.variables.lector import dame

vars_init([claves])

app = Flask(__name__)

rest_init(app, 'apps/routes')

iniciar_db()

if __name__ == "__main__":
    flask_host = dame(claves.Variables.PYTHON_HOST)
    flask_port = int(dame(Variable.PYTHON_PORT))

    app.run(host=flask_host, port=flask_port, debug=True)
