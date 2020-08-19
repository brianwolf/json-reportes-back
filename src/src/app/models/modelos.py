import base64
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from os import path
from typing import List
from uuid import UUID, uuid4


class TipoArchivo(Enum):
    MODELO = 'MODELO'
    REPORTE = 'REPORTE'


@dataclass
class Archivo:
    nombre: str
    tipo: TipoArchivo
    contenido: bytes = bytes('', 'utf-8')
    uuid_guardado: UUID = field(default_factory=uuid4)
    fecha_creacion: datetime = datetime.now()
    id_modelo: int = None
    id: int = None

    def __eq__(self, value):
        if value == None:
            return False
        if self.id and value.id:
            return self.id == value.id
        return self.nombre == value.nombre and self.uuid_guardado == value.uuid_guardado

    def contenido_base64(self) -> str:
        if not self.contenido:
            return None

        contenido_base64 = base64.b64encode(self.contenido)
        return str(contenido_base64, 'utf-8')

    def contenido_str(self) -> str:
        if self.contenido:
            return self.contenido.decode('utf-8')

        return ''

    def to_json(self, contenidos_tambien: bool = False) -> dict:
        d = {
            'nombre': self.nombre,
            'uuid_guardado': str(self.uuid_guardado),
            'tipo': self.tipo.value,
            'fecha_creacion': self.fecha_creacion,
            'id_modelo': self.id_modelo,
            'id': self.id
        }
        if contenidos_tambien:
            d['contenido'] = self.contenido_base64()
        return d


@dataclass
class Modelo:
    nombre: str
    descripcion: str
    fecha_creacion: datetime = datetime.now()
    archivos: List[Archivo] = None
    id: int = None

    def __eq__(self, value):
        if value == None:
            return False
        if self.id and value.id:
            return self.id == value.id
        return self.nombre == value.nombre

    def buscar_archivo(self, nombre: str) -> Archivo:
        for archivo in self.archivos:
            if nombre == archivo.nombre:
                return archivo
        return None

    def agregar_archivo(self, archivo: Archivo):
        self.archivos.append(archivo)

    def borrar_archivo(self, archivo: Archivo):
        self.archivos.remove(archivo)

    def to_json(self, contenidos_tambien: bool = False) -> dict:
        return {
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_creacion': self.fecha_creacion,
            'archivos:': [a.to_json(contenidos_tambien) for a in self.archivos],
            'id': self.id
        }
