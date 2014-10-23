from ..base import BaseHandler


class UnboundViewMeta(type):
    """
    Metaclass that wraps the `view` attribute with `staticmethod`.

    This ensures that the method does not bind to the class unintentionally.
    """
    def __new__(cls, name, bases, attrs):
        """Create the new class with a staticmethod view attribute."""
        view = attrs.get('view')
        if view:
            attrs['view'] = staticmethod(view)
        return super().__new__(cls, name, bases, attrs)


class SimpleHandler(BaseHandler, metaclass=UnboundViewMeta):
    """
    Abstract handler for Routes that have one url: `/` relative to the Route.

    Subclasses should define a view on the class as `view`. This will be
    called if the `path` passed to `handle` is `/`.
    """
    urlconf = 'conman.routes.handlers.simple.urls'
