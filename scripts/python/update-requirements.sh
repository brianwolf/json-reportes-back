. ./scripts/python/ambiente.env

. $CARPETA_ENV/bin/activate &&
    pip install -r $CARPETA_REQUIREMENTS &&\
    pip freeze > $CARPETA_REQUIREMENTS &&\
    deactivate
