. ./scripts/python/ambiente.env

# CREAR VIRTUAL ENV
virtualenv -p python$PYTHON_VERSION $CARPETA_ENV


# INSTALAR DEPENDENCIAS
. ./scripts/python/update-requirements.sh