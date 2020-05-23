import sqlite3
from typing import Iterable, List

from apps.configs.variables.claves import Variable
from apps.configs.variables.lector import dame


def obtener_conexion() -> sqlite3.Connection:
    '''
    Obtiene la conexion con la base de datos SQLite
    '''
    return sqlite3.connect(dame(Variable.DB_SQLITE_RUTA))


def select(consulta: str, parametros: Iterable = [], conexion: sqlite3.Connection = obtener_conexion()) -> List[any]:
    '''
    Ejecuta un select en la conexion parametro.
    '''
    cursor = conexion.cursor()
    cursor.execute(consulta, parametros)
    resultado = cursor.fetchall()

    conexion.close()
    return resultado


def insert(consulta: str, parametros: Iterable = [], conexion: sqlite3.Connection = obtener_conexion()) -> any:
    '''
    Ejecuta un insert en la conexion parametro.
    Devuelve el id insertado
    '''
    cursor = conexion.cursor()
    cursor.execute(consulta, parametros)
    id = cursor.lastrowid

    conexion.commit()
    conexion.close()
    return id


def ejecutar(consulta: str, parametros: Iterable = [], commit: bool = False, conexion: sqlite3.Connection = obtener_conexion()) -> List[any]:
    '''
    Ejecuta una consulta SQL en la conexion parametro.
    En caso de hacer inserts o updates asegurarse de pasar commit=True
    '''
    cursor = conexion.cursor()
    cursor.execute(consulta, parametros)
    resultado = cursor.fetchall()

    if commit:
        conexion.commit()

    conexion.close()
    return resultado
