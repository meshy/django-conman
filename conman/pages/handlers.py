from . import views
from conman.nav_tree.handlers import SimpleHandler


class PageHandler(SimpleHandler):
    view = views.PageDetail.as_view()
