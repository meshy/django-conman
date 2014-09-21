from django.db import models

from conman.nav_tree.models import Node


class NodeRedirect(Node):
    """
    When `node` is browsed to, browser should be redirected to `target`.

    This model holds the data required to make that connection.
    """
    target = models.ForeignKey('nav_tree.Node', related_name='+')
    permanent = models.BooleanField(default=False, blank=True)
