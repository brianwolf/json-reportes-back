from enum import Enum
from typing import List

from apps.configs.sqlite import sqlite
from apps.models.archivos import Archivo, TipoCreador
from apps.models.errores import AppException
from apps.repositories import tipo_creador_repository

_TABLA = 'ARCHIVOS'


def crear(a: Archivo) -> Archivo:
    '''
    Crea un Archivo con sus archivos en la base de datos
    '''
    tipo_creador = tipo_creador_repository.buscar_por_enum(a.tipo_creador)

    consulta = f'''
        INSERT INTO {_TABLA} (NOMBRE, FECHA_CREACION, RUTA_RELATIVA, ID_CREADOR, ID_TIPO_CREADOR)
        VALUES (?,?,?,?,?)
    '''
    parametros = [a.nombre, a.fecha_creacion,
                  a.ruta_relativa, a.id_creador, tipo_creador.id]

    a.id = sqlite.insert(consulta, parametros=parametros)
    return a


def actualizar(id: any, a: Archivo) -> Archivo:
    '''
    Actualiza un Archivo en la base de datos
    '''
    tipo_creador = tipo_creador_repository.buscar_por_enum(a.tipo_creador)

    consulta = f'''
        UPDATE {_TABLA}
        SET NOMBRE=?, FECHA_CREACION=?, RUTA_RELATIVA=?, ID_CREADOR=?, ID_TIPO_CREADOR=?
        WHERE ID = ?
    '''
    parametros = [a.nombre, a.fecha_creacion,
                  a.ruta_relativa, a.id_creador, tipo_creador.id, id]
    sqlite.ejecutar(consulta, parametros=parametros, commit=True)
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
    tipo_creador = tipo_creador_repository.buscar(r[5])

    a = Archivo(id=r[0], nombre=r[1], fecha_creacion=r[2],
                ruta_relativa=r[3], id_creador=r[4], id_tipo_creador=r[5], tipo_creador=tipo_creador.to_enum())

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
    cache = {}
    for r in resultados:

        id_tipo_creador = r[5]
        if id_tipo_creador not in cache:
            cache[id_tipo_creador] = tipo_creador_repository.buscar(
                id_tipo_creador).to_enum()

        archivos.append(Archivo(id=r[0], nombre=r[1], fecha_creacion=r[2],
                                ruta_relativa=r[3], id_creador=r[4], id_tipo_creador=r[5], tipo_creador=cache[id_tipo_creador]))

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
