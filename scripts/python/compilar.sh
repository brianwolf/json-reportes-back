. ./scripts/python/ambiente.sh

. $CARPETA_ENV/bin/activate && 
    pip install compile &&
    compile -b -f -x "env" -o $CARPETA_COMPILADO $CARPETA_CODIGO &&
    deactivate
