from enum import Enum
from typing import List

from apps.configs.sqlite import sqlite
from apps.models.archivos import Archivo, TipoCreador
from apps.models.errores import AppException

_TABLA = 'ARCHIVOS'


def crear(a: Archivo) -> Archivo:
    '''
    Crea un Archivo con sus archivos en la base de datos
    '''
    consulta = f'''
        INSERT INTO {_TABLA} (NOMBRE, FECHA_CREACION, RUTA_RELATIVA, TIPO_CREADOR, ID_CREADOR)
        VALUES (?,?,?,?,?)
    '''
    parametros = [a.nombre, a.fecha_creacion,
                  a.ruta_relativa, a.tipo_creador.value, a.id_creador]

    a.id = sqlite.insert(consulta, parametros=parametros)
    return a


def actualizar(id: any, a: Archivo) -> Archivo:
    '''
    Actualiza un Archivo en la base de datos
    '''
    consulta = f'''
        UPDATE {_TABLA}
        SET NOMBRE=?, FECHA_CREACION=?, RUTA_RELATIVA=?, TIPO_CREADOR=?, ID_CREADOR=?
        WHERE ID = ?
    '''
    parametros = [a.nombre, a.fecha_creacion,
                  a.ruta_relativa, a.tipo_creador.value, a.id_creador, id]
    sqlite.ejecutar(consulta, parametros=parametros, commit=True)
    a.id = id
    return a


def buscar(id: any) -> Archivo:
    '''
    Busca un Archivo por id
    '''
    consulta = f'''
        SELECT *
        FROM {_TABLA}
        WHERE ID = ?
    '''
    r = sqlite.select(consulta, parametros=[id])
    a = Archivo(id=r[0], nombre=r[1], fecha_creacion=r[2],
                ruta_relativa=r[3], tipo_creador=TipoCreador[r[4]], id_creador=r[5])
    return a


def buscar_por_filtros(filtros: dict = None) -> List[Archivo]:
    '''
    Busca Archivos que cumplan con el filtro
    '''
    consulta = f'''
        SELECT * FROM {_TABLA}
    '''
    parametros = []
    if filtros:
        consulta += ' WHERE '
        for k, v in filtros.items():
            consulta += f'{str(k).upper()}=? AND '
            parametros.append(v)

    consulta = consulta[:-len(' AND ')]
    resultados = sqlite.select(consulta, parametros=parametros)

    archivos = []
    for r in resultados:
        archivos.append(Archivo(id=r[0], nombre=r[1], fecha_creacion=r[2],
                                ruta_relativa=r[3], tipo_creador=TipoCreador[r[4]], id_creador=r[5]))

    return archivos


def borrar(id: any):
    '''
    Borra un Archivo por id
    '''
    consulta = f'''
        DELETE FROM {_TABLA}
        WHERE ID = ?
    '''
    r = sqlite.ejecutar(consulta, parametros=[id], commit=True)
