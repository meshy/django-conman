from ..base import BaseHandler


class UnboundViewMeta(type):
    """
    Metaclass that wraps the `view` attribute with `staticmethod`.

    This ensures that the method does not bind to the class unintentionally.
    """
    def __new__(cls, name, bases, attrs):
        view = attrs.get('view')
        if view:
            attrs['view'] = staticmethod(view)
        return super().__new__(cls, name, bases, attrs)


class SimpleHandler(BaseHandler, metaclass=UnboundViewMeta):
    """
    Abstract handler for Nodes that have one url: `/` relative to the Node.

    Subclasses should define a view on the class as `view`. This will be
    called if the `path` passed to `handle` is `/`.
    """
    urlconf = 'conman.nav_tree.handlers.simple.urls'
