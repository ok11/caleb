import uuid
import inspect
import json
import pickle

from .model import Dictable


def generate_id():
    return str(uuid.uuid1())


class DictableEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Dictable):
            return obj.to_dict()
        elif isinstance(obj, (list, dict, str, int, float, bool, type(None))):
            return json.JSONEncoder.default(self, obj)
        elif hasattr(obj, "__dict__"):
            return dict(
                (key, value) for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
        return json.JSONEncoder.default(self, obj)
