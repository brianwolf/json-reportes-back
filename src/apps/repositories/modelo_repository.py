import json
import os
from datetime import datetime
from enum import Enum
from typing import List

import apps.utils.archivos_util as archivos_util
from apps.configs.logger.logger import obtener_logger
from apps.configs.sqlite import sqlite
from apps.models.archivos import Archivo, Carpeta, Modelo, TipoCarpeta
from apps.models.errores import AppException


class Errores(Enum):
    NOMBRE_EN_USO = 'NOMBRE_EN_USO'
    CARPETA_NO_EXISTE = 'CARPETA_NO_EXISTE'


def crear(m: Modelo) -> Modelo:
    '''
    Crea un modelo con sus archivos en la base de datos
    '''
    consulta = f'''
    INSERT INTO MODELOS (NOMBRE, FECHA_CREACION, DESCRIPCION)
    VALUES (?,?,?)
    '''
    parametros = [m.nombre, m.fecha_creacion.isoformat(), m.descripcion]

    m.id = sqlite.ejecutar(consulta, parametros=parametros, commit=True)
    return m


def actualizar(m: Modelo) -> Modelo:
    '''
    Actualiza un modelo en la base de datos
    '''
    consulta = f'''
    INSERT INTO MODELOS (NOMBRE, FECHA_CREACION, DESCRIPCION)
    VALUES (?,?,?)
    '''
    parametros = [m.nombre, m.fecha_creacion.isoformat(), m.descripcion]

    m.id = sqlite.insert(consulta, parametros=parametros, commit=True)
    return m


def buscar(id: any) -> Modelo:
    '''
    Busca un modelo por id
    '''
    consulta = f'''
    SELECT * 
    FROM MODELOS
    WHERE ID = ?
    '''
    r = sqlite.ejecutar(consulta, parametros=[id])
    return Modelo(nombre=r.)


def borrar(carpeta: Carpeta):
    '''
    Borra un Carpeta
    '''
    ruta_completa = archivos_util.ruta_archivo(
        carpeta.tipo.value, carpeta.nombre, _METADATA_NOMBRE)
    os.remove(ruta_completa)


def agregar_archivo(carpeta: Carpeta, archivo: Archivo):
    '''
    Agrega un archivo a la lista de archivos de una carpeta
    '''
    carpeta = buscar_por_nombre(carpeta.nombre)
    carpeta.archivos.append(archivo)

    crear(carpeta)
