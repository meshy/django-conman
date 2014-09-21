from sirtrevor.fields import SirTrevorField

from conman.nav_tree.models import Node


class Page(Node):
    """A basic Page of content provided by Sir Trevor"""
    content = SirTrevorField(default='')
