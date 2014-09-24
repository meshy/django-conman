from . import views
from conman.nav_tree.handlers import SimpleHandler


class NodeRedirectHandler(SimpleHandler):
    view = views.NodeRedirectView.as_view()
