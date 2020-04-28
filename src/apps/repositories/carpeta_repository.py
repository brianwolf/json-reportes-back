from apps.configs.lector_variables import dame
from apps.configs.loggers import get_logger
from apps.configs.variables import Variable
from apps.models.carpeta import Archivo, Carpeta

_REPO = db_por_tipo(dame(Variable.DB_TIPO))
_LOG = get_logger()


def db_por_tipo(tipo: str):
    '''
    Carga un repositorio dependiendo del tipo
    '''
    if tipo == 'sqlite':
        import apps.repositories.sqlite.carpeta_repository as repo
        _LOG.info('Usando BD de sqlite')
        return repo

    import apps.repositories.archivo.carpeta_repository as repo
    _LOG.info('Usando archivo sin BD')
    return repo


class Errores(Enum):
    NOMBRE_EN_USO = 'NOMBRE_EN_USO'
    CARPETA_NO_EXISTE = 'CARPETA_NO_EXISTE'


def crear(carpeta: Carpeta) -> UUID:
    '''
    Crea una Carpeta en la base local de archivos
    '''
    return _REPO.crear(carpeta)


def actualizar(carpeta: Carpeta) -> UUID:
    '''
    Actualiza una Carpeta en la base local de archivos
    '''
    pass


def buscar_por_nombre(nombre: str) -> Carpeta:
    '''
    Busca un Carpeta por nombre
    '''
    return None


def buscar(id: UUID) -> Carpeta:
    '''
    Busca un Carpeta por id
    '''
    pass


def borrar(carpeta: Carpeta):
    '''
    Borra un Carpeta
    '''
    pass


def agregar_archivo(carpeta: Carpeta, archivo: Archivo):
    '''
    Agrega un archivo a la lista de archivos de una carpeta
    '''
    pass
