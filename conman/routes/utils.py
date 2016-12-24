from collections import deque


def split_path(path):
    """
    Split a url path into its sub-paths.

    A url's sub-paths consist of all substrings ending in / and starting at
    the start of the url.

    eg: /path/containing/subpaths/ becomes:

        /
        /path/
        /path/containing/
        /path/containing/subpaths/
    """
    paths = deque()
    path = path or '/'
    while path:
        path = path.rpartition('/')[0]
        paths.appendleft(path + '/')
    return list(paths)
