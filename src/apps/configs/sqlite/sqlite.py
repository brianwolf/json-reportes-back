import sqlite3
from os import path
from typing import Iterable, List

from apps.configs.variables.lector import Variable, dame


def obtener_conexion() -> sqlite3.Connection:
    '''
    Obtiene la conexion con la base de datos SQLite
    '''
    ruta_archivo_sql = dame(Variable.DB_SQLITE_RUTA)
    if not path.exists(ruta_archivo_sql):
        mensaje = f'El arbol de directorios para crear el archivo {ruta_archivo_sql} no existe'
        raise Exception(mensaje)

    return sqlite3.connect(ruta_archivo_sql, check_same_thread=False)


def select(consulta: str, parametros: Iterable = [], conexion: sqlite3.Connection = obtener_conexion()) -> List[any]:
    '''
    Ejecuta un select en la conexion parametro.
    '''
    cursor = conexion.cursor()
    cursor.execute(consulta, parametros)
    resultado = cursor.fetchall()

    cursor.close()
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
    cursor.close()
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

    cursor.close()
    return resultado
