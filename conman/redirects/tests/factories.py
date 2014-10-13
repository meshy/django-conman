import factory

from conman.nav_tree.tests.factories import ChildNodeFactory
from .. import models


class ChildNodeRedirectFactory(ChildNodeFactory):
    target = factory.SubFactory(ChildNodeFactory)

    class Meta:
        model = models.NodeRedirect
