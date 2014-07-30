from ..base import BaseHandler


class SimpleHandler(BaseHandler):
    """
    Abstract handler for Nodes that have one url: `/` relative to the Node.

    Subclasses should define a view on the class as `view`. This will be
    called if the `path` passed to `handle` is `/`.
    """
    urlconf = 'nav_tree.handlers.simple.urls'
