from django.db import models

from conman.nav_tree.models import Node
from . import handlers


class NodeRedirect(Node):
    """
    When `node` is browsed to, browser should be redirected to `target`.

    This model holds the data required to make that connection.
    """
    handler = handlers.NodeRedirectHandler.path()
    target = models.ForeignKey('nav_tree.Node', related_name='+')
    permanent = models.BooleanField(default=False, blank=True)
