from apps.configs.logger.logger import obtener_logger
from apps.configs.variables.lector import Variable, dame
from apps.repositories.models.setup_model import ImplementationRouter, TipoDB

_logger = obtener_logger()


_tipo_db: TipoDB = TipoDB.SQLITE
_router: ImplementationRouter = ImplementationRouter()


def _loggear_tipo_db_usado(tipo_db: TipoDB):
    _logger.info(f'Base de datos en uso -> {tipo_db.value}')


def iniciar_db():
    global _tipo_db, _router
    _tipo_db = TipoDB[dame(Variable.DB_TIPO).upper()]
    _loggear_tipo_db_usado(_tipo_db)

    if _tipo_db == TipoDB.MONGODB:
        pass

    if _tipo_db == TipoDB.SQLITE:
        from apps.repositories.implementations.sqlite import archivo_repository, modelo_repository, setup

    _router.archivo_repository = archivo_repository
    _router.modelo_repository = modelo_repository

    setup.iniciar_db()
