from enum import Enum
from typing import List

from apps.configs.sqlite import sqlite
from apps.models.archivos import Archivo, Carpeta, Modelo, TipoCarpeta
from apps.models.errores import AppException
from apps.repositories import archivo_repository

_TABLA = 'MODELOS'


def crear(m: Modelo) -> Modelo:
    '''
    Crea un modelo con sus archivos en la base de datos
    '''
    consulta = f'''
        INSERT INTO {_TABLA} (NOMBRE, FECHA_CREACION, DESCRIPCION)
        VALUES (?,?,?)
    '''
    parametros = [m.nombre, m.fecha_creacion, m.descripcion]
    m.id = sqlite.insert(consulta, parametros=parametros)

    archivos_insertados = []
    for a in m.archivos:
        a.id_creador = m.id
        archivos_insertados.append(archivo_repository.crear(a))

    m.archivos = archivos_insertados
    return m


def actualizar(id: any, m: Modelo) -> Modelo:
    '''
    Actualiza un modelo en la base de datos
    '''
    consulta = f'''
        UPDATE {_TABLA} 
        SET NOMBRE=?, FECHA_CREACION=?, DESCRIPCION=?
        WHERE ID = ?
    '''
    parametros = [m.nombre, m.fecha_creacion, m.descripcion, id]
    sqlite.ejecutar(consulta, parametros=parametros, commit=True)

    m.id = id
    return m


def buscar(id: any) -> Modelo:
    '''
    Busca un modelo por id
    '''
    consulta = f'''
        SELECT *
        FROM {_TABLA}
        WHERE ID = ?
    '''
    r = sqlite.select(consulta, parametros=[id])
    return Modelo(id=r[0], nombre=r[1], fecha_creacion=r[2], descripcion=[3])


def buscar_por_filtros(filtros: dict = None) -> List[Modelo]:
    '''
    Busca modelos que cumplan con el filtro
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

    return [Modelo(id=r[0], nombre=r[1], fecha_creacion=r[2], descripcion=r[3]) for r in resultados]


def borrar(id: any):
    '''
    Borra un modelo por id
    '''
    consulta = f'''
        DELETE FROM {_TABLA}
        WHERE ID = ?
    '''
    r = sqlite.ejecutar(consulta, parametros=[id], commit=True)
