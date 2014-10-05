from conman.nav_tree.tests.factories import RootNodeFactory
from .. import handlers, models


class PageFactory(RootNodeFactory):
    handler = handlers.PageHandler.path()

    class Meta:
        model = models.Page
