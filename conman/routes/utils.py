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
        paths.insert(1, path + '/')
        path = os.path.split(path)[0]
        if path == '/':
            break
    return paths
