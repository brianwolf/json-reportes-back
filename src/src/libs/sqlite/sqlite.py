'''
SQLite
------

Contiene metodos basicos para el uso de un sqlite
'''
import os
import sqlite3
from typing import Iterable, List

from src.libs.sqlite.src import config
from src.libs.sqlite.src.sistema_archivos import _crear_arbol_de_directorios


def iniciar(ruta_archivo_sqlite_predefinida: str):
    '''
    Crea el arbol de directorios necesario para que sqlite cree su archivo .db
    '''
    config.RUTA_DB_PREDEFINIDA = ruta_archivo_sqlite_predefinida


def obtener_conexion(ruta_archivo_sqlite: str) -> sqlite3.Connection:
    '''
    Obtiene la conexion con la base de datos SQLite
    '''
    _crear_arbol_de_directorios(ruta_archivo_sqlite)
    return sqlite3.connect(ruta_archivo_sqlite, check_same_thread=False)


def select(consulta: str, parametros: Iterable = [], conexion: sqlite3.Connection = None) -> List[any]:
    '''
    Ejecuta un select en la conexion parametro.
    '''
    if conexion == None:
        conexion = obtener_conexion(config.RUTA_DB_PREDEFINIDA)

    cursor = conexion.cursor()
    cursor.execute(consulta, parametros)
    resultado = cursor.fetchall()

    cursor.close()
    return resultado


def insert(consulta: str, parametros: Iterable = [], conexion: sqlite3.Connection = None) -> any:
    '''
    Ejecuta un insert en la conexion parametro.
    Devuelve el id insertado
    '''
    if conexion == None:
        conexion = obtener_conexion(config.RUTA_DB_PREDEFINIDA)

    cursor = conexion.cursor()
    cursor.execute(consulta, parametros)
    id = cursor.lastrowid

    conexion.commit()
    cursor.close()
    return id


def ejecutar(consulta: str, parametros: Iterable = [], commit: bool = False, conexion: sqlite3.Connection = None) -> List[any]:
    '''
    Ejecuta una consulta SQL en la conexion parametro.
    En caso de hacer inserts o updates asegurarse de pasar commit=True
    '''
    if conexion == None:
        conexion = obtener_conexion(config.RUTA_DB_PREDEFINIDA)

    cursor = conexion.cursor()
    cursor.execute(consulta, parametros)
    resultado = cursor.fetchall()

    if commit:
        conexion.commit()

    cursor.close()
    return resultado


def ejecutar_script(ruta_script: str, commit: bool = False, conexion: sqlite3.Connection = None) -> List[any]:
    '''
    Ejecuta un script ubicado en la ruta enviada por parametro.
    En caso de hacer inserts o updates asegurarse de pasar commit=True
    '''
    if conexion == None:
        conexion = obtener_conexion(config.RUTA_DB_PREDEFINIDA)

    with open(ruta_script, mode='r') as script_archivo:
        contenido_script = script_archivo.read()

    cursor = conexion.cursor()
    cursor.executescript(contenido_script)
    resultado = cursor.fetchall()

    if commit:
        conexion.commit()

    cursor.close()
    return resultado
