from datetime import date

from flask.json import JSONEncoder

__version__ = '1.0.0'


class JSONEncoderPersonalizado(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
