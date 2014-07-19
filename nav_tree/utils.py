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
