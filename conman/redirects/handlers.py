from conman.url_tree.handlers import SimpleHandler
from . import views


class NodeRedirectHandler(SimpleHandler):
    view = views.NodeRedirectView.as_view()
