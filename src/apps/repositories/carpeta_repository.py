import os
from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID, uuid4

import apps.configs.variables as var
import apps.utils.archivos_util as archivos_util
from apps.configs.loggers import get_logger
from apps.models.carpeta import Archivo, Carpeta, TipoCarpeta
from apps.models.errores import AppException
import json


class Errores(Enum):
    NOMBRE_EN_USO = 'NOMBRE_EN_USO'
    CARPETA_NO_EXISTE = 'CARPETA_NO_EXISTE'


def guardar(carpeta: Carpeta) -> UUID:
    '''
    Guarda un Carpeta en la base local de archivos
    '''
    ruta_carpeta = archivos_util.ruta_tipo_carpeta(carpeta.tipo.value,
                                                   carpeta.nombre)

    nombre_en_uso = carpeta.nombre in archivos_util.listado_archivos_directorio_base()
    if nombre_en_uso:
        mensaje = f'El nombre {carpeta.nombre} ya esta en uso'
        raise AppException(Errores.NOMBRE_EN_USO, mensaje)

    carpeta.id = uuid4()

    carpeta_dict = carpeta.to_dict()
    for archivo in carpeta_dict['archivos']:
        del archivo['contenido']

    contenido = json.dumps(carpeta_dict).encode('utf8')

    archivos_util.guardar_archivo(ruta_carpeta,
                                  _nombre_meta_data(carpeta.nombre), contenido)

    return carpeta.id


def buscar_por_nombre(nombre: str) -> Carpeta:
    '''
    Busca un Carpeta por nombre
    '''
    ruta_completa = archivos_util.ruta_tipo_carpeta(
        TipoCarpeta.MODELO.value, nombre) + _nombre_meta_data(nombre)

    if not os.path.exists(ruta_completa):
        mensaje = f'La carpeta {nombre} NO existe'
        raise AppException(Errores.CARPETA_NO_EXISTE, mensaje)

    metadata_contenido = archivos_util.obtener_archivo(ruta_completa)
    metadata_dict = json.loads(metadata_contenido.decode('utf8'))

    return Carpeta.from_dict(metadata_dict)


def borrar(carpeta: Carpeta):
    '''
    Borra un Carpeta
    '''
    ruta_completa = archivos_util.ruta_tipo_carpeta(
        carpeta.tipo.value, carpeta.nombre) + _nombre_meta_data(carpeta.nombre)

    os.remove(ruta_completa)


def agregar_archivo(carpeta: Carpeta, archivo: Archivo):
    '''
    Agrega un archivo a la lista de archivos de una carpeta
    '''
    carpeta = buscar_por_nombre(carpeta.nombre)
    carpeta.archivos.append(archivo)

    guardar(carpeta)


def _nombre_meta_data(nombre_carpeta: str):
    return f'.{nombre_carpeta}.json'
