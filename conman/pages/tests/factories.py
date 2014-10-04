from conman.nav_tree.tests.factories import RootNodeFactory
from .. import models


class PageFactory(RootNodeFactory):
    class Meta:
        model = models.Page
