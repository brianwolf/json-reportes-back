from enum import Enum
from typing import List

from apps.configs.sqlite import sqlite
from apps.models.errores import AppException
from apps.models.modelos import Archivo, Modelo
from apps.repositories import archivo_repository

_TABLA = 'MODELOS'


def listado_modelos() -> List[str]:
    '''
    Crea un modelo con sus archivos en la base de datos
    '''
    consulta = f'SELECT NOMBRE FROM {_TABLA}'
    resultado = sqlite.select(consulta, parametros=[])
    return [r[0] for r in resultado]


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

    return m


def actualizar(m: Modelo) -> Modelo:
    '''
    Actualiza un modelo en la base de datos
    '''
    consulta = f'''
        UPDATE {_TABLA} 
        SET NOMBRE=?, FECHA_CREACION=?, DESCRIPCION=?
        WHERE ID = ?
    '''
    parametros = [m.nombre, m.fecha_creacion, m.descripcion, m.id]
    sqlite.ejecutar(consulta, parametros=parametros, commit=True)

    # archivos_viejos = archivo_repository.buscar_por_filtros(
    #     {'ID_MODELO': m.id})
    # for av in archivos_viejos:
    #     archivo_repository.borrar(av.id)

    # archivos_nuevos = []
    # for a in m.archivos:
    #     a.id_modelo = m.id
    #     archivos_nuevos.append(archivo_repository.crear(a))

    # m.archivos = archivos_nuevos
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
    m = Modelo(id=r[0], nombre=r[1], fecha_creacion=r[2], descripcion=[3])

    m.archivos = archivo_repository.buscar_por_filtros({'ID_MODELO': m.id})
    return m


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

    modelos = [Modelo(id=r[0], nombre=r[1], fecha_creacion=r[2],
                      descripcion=r[3]) for r in resultados]
    for m in modelos:
        m.archivos = archivo_repository.buscar_por_filtros(
            {'ID_MODELO': m.id})
    return modelos


def buscar_por_nombre(nombre: str) -> Modelo:
    '''
    Busca un modelo por su nombre
    '''
    resultado = buscar_por_filtros({'NOMBRE': nombre})
    if not resultado:
        return None

    return resultado[0]


def borrar(id: any):
    '''
    Borra un modelo por id
    '''
    consulta = f'''
        DELETE FROM {_TABLA}
        WHERE ID = ?
    '''
    r = sqlite.ejecutar(consulta, parametros=[id], commit=True)

    for a in archivo_repository.buscar_por_filtros({'ID_MODELO': id}):
        archivo_repository.borrar(a.id)
