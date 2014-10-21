from django.db import models

from conman.routes.models import Node
from . import handlers


class NodeRedirect(Node):
    """
    When `node` is browsed to, browser should be redirected to `target`.

    This model holds the data required to make that connection.
    """
    handler = handlers.NodeRedirectHandler.path()
    target = models.ForeignKey('routes.Node', related_name='+')
    permanent = models.BooleanField(default=False, blank=True)
