from django.db import models

from conman.routes.models import Route
from . import handlers


class RouteRedirect(Route):
    """
    When `route` is browsed to, browser should be redirected to `target`.

    This model holds the data required to make that connection.
    """
    handler = handlers.RouteRedirectHandler.path()
    target = models.ForeignKey('routes.Route', related_name='+')
    permanent = models.BooleanField(default=False, blank=True)
