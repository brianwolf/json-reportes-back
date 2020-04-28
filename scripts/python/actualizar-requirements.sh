. ./scripts/python/ambiente.sh

. $CARPETA_ENV/bin/activate &&
    pip install -r $CARPETA_REQUIREMENTS --upgrade pip &&\
    pip freeze > $CARPETA_REQUIREMENTS &&\
    deactivate
