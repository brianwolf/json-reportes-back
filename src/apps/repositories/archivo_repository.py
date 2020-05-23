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
        INSERT INTO {_TABLA} (NOMBRE, FECHA_CREACION, DESCRIPCION)
        VALUES (?,?,?)
    '''
    parametros = [a.nombre, a.fecha_creacion, a.descripcion]
    a.id = sqlite.insert(consulta, parametros=parametros)
    return a


def actualizar(id: any, a: Archivo) -> Archivo:
    '''
    Actualiza un Archivo en la base de datos
    '''
    consulta = f'''
        UPDATE {_TABLA} 
        SET NOMBRE=?, FECHA_CREACION=?, DESCRIPCION=?
        WHERE ID = ?
    '''
    parametros = [a.nombre, a.fecha_creacion, a.descripcion, id]
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
    return Archivo(id=r[0], nombre=r[1], fecha_creacion=r[2], descripcion=[3])


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
    r = sqlite.select(consulta, parametros=parametros)

    return Archivo(id=r[0], nombre=r[1], fecha_creacion=r[2], descripcion=[3])


def borrar(id: any):
    '''
    Borra un Archivo por id
    '''
    consulta = f'''
        DELETE FROM {_TABLA}
        WHERE ID = ?
    '''
    r = sqlite.ejecutar(consulta, parametros=[id], commit=True)
    return Archivo(id=r[0], nombre=r[1], fecha_creacion=r[2], descripcion=[3])
