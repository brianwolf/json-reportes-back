import base64
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID, uuid4

import apps.configs.variables as var
import apps.utils.archivos_util as util_archi


class Archivo():
    def __init__(self,
                 nombre: str,
                 contenido: bytes = bytes('', 'utf-8'),
                 fecha_creacion: datetime = datetime.now()):

        self.nombre = nombre
        self.contenido = contenido
        self.fecha_creacion = fecha_creacion

    def to_dict(self):
        d = {
            'nombre': self.nombre,
            'fecha_creacion': str(self.fecha_creacion)
        }

        if self.contenido:
            d['contenido'] = self.contenido_base64()

        return d

    def contenido_base64(self):
        if self.contenido:
            contenido_base64 = base64.b64encode(self.contenido)
            return str(contenido_base64, 'utf-8')

        return ''

    def contenido_str(self):
        if self.contenido:
            return self.contenido.decode('utf-8')

        return ''

    @staticmethod
    def from_dict(d: dict):
        return Archivo(**d)


class TipoCarpeta(Enum):
    MODELO = 'MODELO'
    PDF = 'PDF'
    MARKDOWN = 'MARCKDOWN'


class Carpeta():
    def __init__(self,
                 nombre: str,
                 tipo: TipoCarpeta,
                 archivos: list = [],
                 id: UUID = None,
                 fecha_creacion=datetime.now()):
        self.nombre = nombre
        self.tipo = tipo
        self.archivos = archivos
        self.id = id
        self.fecha_creacion = fecha_creacion

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'archivos': [archivo.to_dict() for archivo in self.archivos],
            'id': str(self.id),
            'fecha_creacion': str(self.fecha_creacion),
            'tipo': self.tipo.value
        }

    def buscar_archivo(self, nombre: str) -> Archivo:
        for archivo in self.archivos:
            if nombre == archivo.nombre:
                return archivo

    @staticmethod
    def from_dict(d: dict):
        instancia = Carpeta(**d)

        archivos = []
        for archivo_dict in d['archivos']:
            archivos.append(Archivo.from_dict(archivo_dict))

        instancia.archivos = archivos
        instancia.tipo = TipoCarpeta[d['tipo']]

        return instancia
