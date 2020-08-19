from src.libs.logger.logger import log
from src.libs.sqlite import sqlite
from src.libs.variables.variables import dame
from src.app.configs.variables import Variable


def _db_ya_fue_creada() -> bool:
    '''
    Hace una consulta basica para saber si la base de datos ya fue creada anteriormente
    '''
    try:
        if sqlite.select('SELECT NAME FROM sqlite_master'):
            return True
    except Exception:
        return False
    return False


def _crear_db_por_primera_vez():
    '''
    Crea la base de datos por primera vez ejecutando un script que crea las tablas requeridas
    '''
    ruta_script = dame(Variable.DB_SQLITE_SCRIPT)
    log().info(
        f'iniciar_db() -> Ejecutando script SQL ubicado en {ruta_script}')

    sqlite.ejecutar_script(ruta_script, True)

    log().info(
        f'iniciar_db() -> Terminado')


def iniciar_db():
    '''
    Crea la base de datos de SQLite
    '''
    ruta_db_sqlite = dame(Variable.DB_SQLITE_RUTA)

    sqlite.iniciar(ruta_db_sqlite)
    log().info(
        f'iniciar_db() -> Conectando con la base de datos SQLite ubicada en {ruta_db_sqlite}')

    if not _db_ya_fue_creada():
        _crear_db_por_primera_vez()


if __name__ == "__main__":
    iniciar_db()
