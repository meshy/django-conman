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
    """
    Imports an object (class/module/etc) from a python path string.

    The path must have at least one dot.
    """
    module_path, attr = path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr)
