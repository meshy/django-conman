from sirtrevor.fields import SirTrevorField

from . import handlers
from conman.nav_tree.models import Node


class Page(Node):
    """A basic Page of content provided by Sir Trevor"""
    handler = handlers.PageHandler.path()
    content = SirTrevorField(default='')
