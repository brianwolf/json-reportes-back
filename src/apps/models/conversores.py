from dataclasses import dataclass
from enum import Enum

from apps.models.modelos import Archivo


class ExtensionArchivo(Enum):
    TEXTO = 'TEXTO'
    MD = 'MD'
    HTML = 'HTML'
    PDF = 'PDF'


@dataclass
class ParametrosCrearReporte:
    a_origen: Archivo
    e_origen: ExtensionArchivo
    a_destino: Archivo
    e_destino: ExtensionArchivo
    datos: dict
    guardar: bool = True
