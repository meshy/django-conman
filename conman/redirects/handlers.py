from conman.nav_tree.handlers import SimpleHandler
from . import views


class NodeRedirectHandler(SimpleHandler):
    """Pass a request through to NodeRedirectView."""
    view = views.NodeRedirectView.as_view()
