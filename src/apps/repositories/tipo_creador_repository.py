from enum import Enum
from typing import List

from apps.configs.sqlite import sqlite
from apps.models.archivos import TipoCreador, TipoCreadorEnum
from apps.models.errores import AppException

_TABLA = 'TIPOS_CREADORES'


def buscar(id: any) -> TipoCreador:
    '''
    Busca un TipoCreador por id
    '''
    consulta = f'''
        SELECT *
        FROM {_TABLA}
        WHERE ID = ?
    '''
    r = sqlite.select(consulta, parametros=[id])
    return TipoCreador(id=r[0], nombre=r[1])


def buscar_por_filtros(filtros: dict = None) -> List[TipoCreador]:
    '''
    Busca TipoCreador que cumplan con el filtro
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

    return [TipoCreador(id=r[0], nombre=r[1]) for r in resultados]


def buscar_por_enum(e: TipoCreadorEnum) -> TipoCreador:
    '''
    Busca TipoCreador por enum
    '''
    consulta = f'''
        SELECT * FROM {_TABLA}
        WHERE NOMBRE = ?
    '''
    r = sqlite.select(consulta, parametros=[e.value])
    return TipoCreador(id=r[0], nombre=r[1])
