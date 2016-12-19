from django.db import models
from polymorphic.base import PolymorphicModelBase
from polymorphic.models import PolymorphicModel

from .handlers import RouteViewHandler
from .managers import RouteManager
from .utils import import_from_dotted_path
from .validators import (
    validate_end_in_slash,
    validate_no_dotty_subpaths,
    validate_no_double_slashes,
    validate_no_hash_symbol,
    validate_no_questionmark,
    validate_start_in_slash,
)


class UnboundViewMeta(PolymorphicModelBase):
    """
    Metaclass that wraps the `view` attribute with `staticmethod`.

    This ensures that the view does not bind to the class unintentionally.
    """
    def __new__(cls, name, bases, attrs):
        """
        Create the new class.

        Ensure any `view` attribute is a staticmethod is unbound to the class.
        """
        view = attrs.get('view')
        if view:
            attrs['view'] = staticmethod(view)
        return super().__new__(cls, name, bases, attrs)


class Route(PolymorphicModel, metaclass=UnboundViewMeta):
    """A Route in a tree of url endpoints."""
    url = models.TextField(
        db_index=True,
        validators=[
            validate_end_in_slash,
            validate_start_in_slash,
            validate_no_dotty_subpaths,
            validate_no_double_slashes,
            validate_no_hash_symbol,
            validate_no_questionmark,
        ],
        unique=True,
    )

    objects = RouteManager()
    handler = RouteViewHandler.path()

    def __str__(self):
        """Display a Route's class and url."""
        return '{} @ {}'.format(self.__class__.__name__, self.url)

    def get_descendants(self):
        """Get all the descendants of this Route."""
        if not self.pk:
            return Route.objects.none()
        others = Route.objects.exclude(pk=self.pk)
        descendants = others.filter(url__startswith=self.url)
        return descendants.order_by('url')

    def get_handler_class(self):
        """Import a class from the python path string in `self.handler`."""
        return import_from_dotted_path(self.handler)

    def get_handler(self):
        """
        Get an instance of the handler for this Route instance.

        Multiple calls to this method (on the same instance of Route) will
        return the same instance of handler.
        """
        try:
            return self._handler
        except AttributeError:
            self._handler = self.get_handler_class()(self)
            return self._handler

    def handle(self, request, path):
        """
        Delegate handling the request to the handler.

        The path of this route is chopped off the url to save the handler from
        needing to deal with it. If it really needs it, it will be able to
        derive it from the route (self) that is passed to it on instantiation.
        """
        handler = self.get_handler()
        # Strip the route url from the rest of the path
        path = path[len(self.url) - 1:]
        # Deal with the request
        return handler.handle(request, path)
