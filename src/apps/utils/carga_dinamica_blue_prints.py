'''
Herramienta que carga de formma dinamica los blueprints de flask recursivamente
que se encuentren en un directorio
'''
import imp
import re
from os import path, listdir

from flask import Flask

__version__ = '1.1.0'


def _nombre_archivo(ruta: str, extension=''):
    '''
    Devuelve el nombre del archivo al final de la ruta sin la extension
    '''
    return re.split('/', ruta)[-1].replace(extension, '')


def _cargar_rutas_de_archivos(ruta_base: str):
    '''
    Obtiene las rutas de todos los archivos .py dentro del directorio parametro, 
    es recursivo por lo que si hay carpetas dentro tambien busca ahi
    '''
    sub_rutas = listdir(ruta_base)
    if '__pycache__' in sub_rutas:
        sub_rutas.remove('__pycache__')

    rutas_archivos = []
    directorios = []
    for i in sub_rutas:
        ruta_completa = path.join(ruta_base, i)

        if path.isfile(ruta_completa):
            rutas_archivos.append(ruta_completa)

        if path.isdir(ruta_completa):
            directorios.append(ruta_completa)

    for d in directorios:
        rutas_archivos.extend(_cargar_rutas_de_archivos(d))

    return rutas_archivos


def registrar_blue_prints(app: Flask, directorio_rutas: str):
    '''
    Registra todos los archivos .py del directorio como rutas para Flask,
    para esto los modulos deben tener estos 2 atributos:

    from flask import Blueprint\n
    blue_print = Blueprint('tu_nombre_de_ruta', __name__, url_prefix='/ejemplos')\n
    '''
    rutas = _cargar_rutas_de_archivos(directorio_rutas)

    for ruta_archivo in rutas:

        nombre_archivo = _nombre_archivo(ruta_archivo, '.py')
        modulo = imp.load_source(nombre_archivo, ruta_archivo)

        app.register_blueprint(modulo.blue_print)
