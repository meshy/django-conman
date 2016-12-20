from django.db import models
from polymorphic.models import PolymorphicModel

from .handlers import RouteViewHandler
from .managers import RouteManager
from .validators import (
    validate_end_in_slash,
    validate_no_dotty_subpaths,
    validate_no_double_slashes,
    validate_no_hash_symbol,
    validate_no_questionmark,
    validate_start_in_slash,
)


class Route(PolymorphicModel):
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
    handler_class = RouteViewHandler

    def __str__(self):
        """Display a Route's class and url."""
        return '{} @ {}'.format(self.__class__.__name__, self.url)

    @classmethod
    def check(cls):
        """Delegate model checks to the handler."""
        return cls.handler_class.check(cls)

    def get_descendants(self):
        """Get all the descendants of this Route."""
        if not self.pk:
            return Route.objects.none()
        others = Route.objects.exclude(pk=self.pk)
        descendants = others.filter(url__startswith=self.url)
        return descendants.order_by('url')

    def get_handler(self):
        """
        Get an instance of the handler for this Route instance.

        Multiple calls to this method (on the same instance of Route) will
        return the same instance of handler.
        """
        try:
            return self._handler
        except AttributeError:
            self._handler = self.handler_class(self)
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
