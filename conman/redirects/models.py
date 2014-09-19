from django.db import models


class NodeRedirect(models.Model):
    """
    When `node` is browsed to, browser should be redirected to `target`.

    This model holds the data required to make that connection.
    """
    node = models.OneToOneField('nav_tree.Node', related_name='+')
    target = models.ForeignKey('nav_tree.Node', related_name='+')
    permanent = models.BooleanField(default=False, blank=True)
