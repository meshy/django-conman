from sirtrevor.fields import SirTrevorField

from conman.routes.models import Route
from . import handlers


class Page(Route):
    """A basic Page of content provided by Sir Trevor."""
    handler = handlers.PageHandler.path()
    content = SirTrevorField(default='')
