from ..base import BaseHandler


class UnboundViewMeta(type):
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
    urlconf = 'nav_tree.handlers.simple.urls'
