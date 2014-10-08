import importlib
import os


def split_path(path):
    """
    Split a url path into its sub-paths.

    A url's sub-paths consist of all substrings ending in / and starting at
    the start of the url.
    """
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
    Import an object (class/module/etc) from a python path string.

    The path must have at least one dot.
    """
    module_path, attr = path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr)
