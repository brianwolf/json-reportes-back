import sqlite3
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from apps.configs.sqlite import sqlite
from apps.configs.variables.claves import Variable
from apps.configs.variables.lector import dame

consulta = f'''
INSERT INTO MODELOS (NOMBRE, FECHA_CREACION, DESCRIPCION)
VALUES (?,?,?)
'''
parametros = [str(uuid4()), datetime.now(), 'm.descripcion']

resultado = sqlite.insert(consulta, parametros=parametros)
print(resultado)

consulta = f'''
SELECT * FROM MODELOS
'''
resultado = sqlite.select(consulta)
print(resultado)


print(resultado[0]['NOMBRE'])