CMD gunicorn \
    -b ${PYTHON_HOST}:$PORT \
    --reload \
    --workers=${PYTHON_GUNICORN_WORKERS} \
    --worker-connections=${PYTHON_GUNICORN_CONNECTIONS} \
    ${PYTHON_NOMBRE_APP}:${PYTHON_NOMBRE_FUNCION_APP}

