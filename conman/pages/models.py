from django.db import models
from sirtrevor.fields import SirTrevorField


class Page(models.Model):
    """A basic Page of content provided by Sir Trevor"""
    node = models.OneToOneField('nav_tree.Node', related_name='+')
    content = SirTrevorField(default='')
