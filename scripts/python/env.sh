. ./scripts/python/ambiente.sh

# CREAR VIRTUAL ENV
virtualenv -p python$PYTHON_VERSION $CARPETA_ENV


# INSTALAR DEPENDENCIAS
. ./scripts/python/actualizar-requirements.sh