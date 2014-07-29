import importlib
import os


def split_path(path):
    paths = ['/']
    path = path.rstrip('/')

    while path:
        paths.append(path + '/')
        path = os.path.split(path)[0]
        if path == '/':
            break
    return paths


def import_from_dotted_path(path):
    """Imports a class from a python path string.

    Must have at least one dot."""
    module_name, class_name = path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)
