. ./scripts/python/ambiente.sh

. $CARPETA_ENV/bin/activate &&
    pip freeze >$RUTA_REQUIREMENTS &&
    deactivate
