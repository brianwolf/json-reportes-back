_directorio_logs = 'produce/logs'
_nivel_logs = 'INFO'


def init(directorio: str, nivel: str):
    '''
    Configura el logger para el proyecto
    '''
    global _directorio_logs, nivel_logs

    _directorio_logs = directorio
    _nivel_logs = nivel
