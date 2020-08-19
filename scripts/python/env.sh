. ./scripts/python/ambiente.sh

virtualenv -p python$PYTHON_VERSION $CARPETA_ENV

. $CARPETA_ENV/bin/activate &&
    pip install -r $RUTA_REQUIREMENTS --upgrade pip
