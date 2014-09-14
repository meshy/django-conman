import factory

from .. import models
from conman.nav_tree.tests.factories import RootNodeFactory


class PageFactory(factory.DjangoModelFactory):
    node = factory.SubFactory(RootNodeFactory)

    class Meta:
        model = models.Page
