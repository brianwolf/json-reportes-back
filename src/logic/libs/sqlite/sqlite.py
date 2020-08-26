"""
SQLite
------

Contiene metodos basicos para el uso de un sqlite
"""
import sqlite3
from typing import List

from logic.libs.sqlite.src import config
from logic.libs.sqlite.src.sistema_archivos import crear_arbol_de_directorios


def iniciar(ruta_archivo_sqlite_predefinida: str):
    """
    Crea el arbol de directorios necesario para que sqlite cree su archivo .db
    """
    config.RUTA_DB_PREDEFINIDA = ruta_archivo_sqlite_predefinida


def obtener_conexion(ruta_archivo_sqlite: str) -> sqlite3.Connection:
    """
    Obtiene la conexion con la base de datos SQLite
    """
    crear_arbol_de_directorios(ruta_archivo_sqlite)
    return sqlite3.connect(ruta_archivo_sqlite, check_same_thread=False)


def select(consulta: str, parametros=None, conexion: sqlite3.Connection = None) -> List[any]:
    """
    Ejecuta un select en la conexion parametro.
    """
    if parametros is None:
        parametros = []
    if conexion is None:
        conexion = obtener_conexion(config.RUTA_DB_PREDEFINIDA)

    cursor = conexion.cursor()
    cursor.execute(consulta, parametros)
    resultado = cursor.fetchall()

    cursor.close()
    return resultado


def insert(consulta: str, parametros=None, conexion: sqlite3.Connection = None) -> any:
    """
    Ejecuta un insert en la conexion parametro.
    Devuelve el id insertado
    """
    if parametros is None:
        parametros = []
    if conexion is None:
        conexion = obtener_conexion(config.RUTA_DB_PREDEFINIDA)

    cursor = conexion.cursor()
    cursor.execute(consulta, parametros)
    id_insertado = cursor.lastrowid

    conexion.commit()
    cursor.close()
    return id_insertado


def ejecutar(consulta: str, parametros=None, commit: bool = False, conexion: sqlite3.Connection = None) -> \
        List[any]:
    """
    Ejecuta una consulta SQL en la conexion parametro.
    En caso de hacer inserts o updates asegurarse de pasar commit=True
    """
    if parametros is None:
        parametros = []
    if conexion is None:
        conexion = obtener_conexion(config.RUTA_DB_PREDEFINIDA)

    cursor = conexion.cursor()
    cursor.execute(consulta, parametros)
    resultado = cursor.fetchall()

    if commit:
        conexion.commit()

    cursor.close()
    return resultado


def ejecutar_script(ruta_script: str, commit: bool = False, conexion: sqlite3.Connection = None) -> List[any]:
    """
    Ejecuta un script ubicado en la ruta enviada por parametro.
    En caso de hacer inserts o updates asegurarse de pasar commit=True
    """
    if conexion is None:
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
