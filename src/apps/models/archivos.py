import base64
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List


class TipoCreador(Enum):
    MODELO = 'MODELO'
    REPORTE = 'REPORTE'


@dataclass
class Archivo:
    nombre: str
    ruta_relativa: str
    tipo_creador: TipoCreador
    contenido: bytes = bytes('', 'utf-8')
    fecha_creacion: datetime = datetime.now()

    id_tipo_creador: int = None
    id_creador: int = None
    id: int = None

    def __eq__(self, value):
        if value == None:
            return False
        if self.id:
            return self.id == value.id
        return self.nombre == value.nombre

    def contenido_base64(self) -> str:
        if self.contenido:
            contenido_base64 = base64.b64encode(self.contenido)
            return str(contenido_base64, 'utf-8')

        return ''

    def contenido_str(self) -> str:
        if self.contenido:
            return self.contenido.decode('utf-8')

        return ''


@dataclass
class _ContenedorArchivos:
    archivos: List[Archivo] = []

    def buscar_archivo(self, nombre: str) -> Archivo:
        for archivo in self.archivos:
            if nombre == archivo.nombre:
                return archivo

    def agregar_archivo(self, archivo: Archivo):
        self.archivos.append(archivo)

    def borrar_archivo(self, archivo: Archivo):
        self.archivos.remove(archivo)


@dataclass
class Modelo(_ContenedorArchivos):
    nombre: str
    descripcion: str
    fecha_creacion: datetime = datetime.now()
    id: int = None

    def __eq__(self, value):
        if value == None:
            return False
        if self.id:
            return self.id == value.id
        return self.nombre == value.nombre


@dataclass
class Reporte(_ContenedorArchivos):
    nombre: str
    fecha_creacion: datetime = datetime.now()
    id_modelo: int = None
    id: int = None

    def __eq__(self, value):
        if value == None:
            return False
        if self.id:
            return self.id == value.id
        return self.nombre == value.nombre
