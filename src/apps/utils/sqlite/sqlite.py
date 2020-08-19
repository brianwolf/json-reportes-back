import os
import sqlite3
from typing import Iterable, List

from apps.config.variables import Variable
from apps.utils.variables.variables import dame


def _crear_arbol_de_directorios(ruta_archivo_sqlite: str):
    '''
    Crea el arbol de directorios necesario para que sqlite cree su archivo .db
    '''
    if os.path.exists(ruta_archivo_sqlite):
        return

    directorio = ruta_archivo_sqlite
    if ruta_archivo_sqlite.endswith('.db'):
        directorio = os.path.dirname(ruta_archivo_sqlite)

    os.makedirs(directorio, exist_ok=True)


def obtener_conexion() -> sqlite3.Connection:
    '''
    Obtiene la conexion con la base de datos SQLite
    '''
    ruta_archivo_sqlite = dame(Variable.DB_SQLITE_RUTA)
    _crear_arbol_de_directorios(ruta_archivo_sqlite)

    return sqlite3.connect(ruta_archivo_sqlite, check_same_thread=False)


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
