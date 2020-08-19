from apps.repositories.models.setup_model import TipoDB, tipo_db_usado
from apps.utils.logger.logger import log


def _iniciar_sqlite():
    from apps.repositories.implementations.sqlite import setup
    setup.iniciar_db()


def _iniciar_mongodb():
    pass


def iniciar_db():

    log().info(f'Base de datos en uso -> {tipo_db_usado()}')

    if tipo_db_usado() == TipoDB.MONGODB:
        _iniciar_mongodb()
        return

    _iniciar_sqlite()
