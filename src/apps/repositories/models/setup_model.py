from dataclasses import dataclass
from enum import Enum
from typing import Any


class TipoDB(Enum):
    SQLITE = 'SQLITE'
    MONGODB = 'MONGODB'


@dataclass
class ImplementationRouter:
    archivo_repository: Any = None
    modelo_repository: Any = None
