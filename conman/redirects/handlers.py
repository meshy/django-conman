from conman.routes.handlers import SimpleHandler
from . import views


class RouteRedirectHandler(SimpleHandler):
    """Pass a request through to RouteRedirectView."""
    view = views.RouteRedirectView.as_view()
