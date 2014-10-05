from conman.nav_tree.handlers import SimpleHandler
from . import views


class PageHandler(SimpleHandler):
    view = views.PageDetail.as_view()
