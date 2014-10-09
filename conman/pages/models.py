from sirtrevor.fields import SirTrevorField

from conman.url_tree.models import Node
from . import handlers


class Page(Node):
    """A basic Page of content provided by Sir Trevor"""
    handler = handlers.PageHandler.path()
    content = SirTrevorField(default='')
