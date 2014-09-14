from django.db import models
from sirtrevor.fields import SirTrevorField


class Page(models.Model):
    node = models.ForeignKey('nav_tree.Node', related_name='+')
    content = SirTrevorField(default='')
