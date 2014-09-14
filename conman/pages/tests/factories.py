import factory

from .. import handlers, models
from conman.nav_tree.tests.factories import RootNodeFactory


class PageFactory(factory.DjangoModelFactory):
    node = factory.SubFactory(RootNodeFactory, handler=handlers.PageHandler.path())

    class Meta:
        model = models.Page
