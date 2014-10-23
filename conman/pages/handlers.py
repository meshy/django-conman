from conman.routes.handlers import SimpleHandler
from . import views


class PageHandler(SimpleHandler):
    """Pass a request to PageDetail."""
    view = views.PageDetail.as_view()
