import factory

from conman.nav_tree.tests.factories import ChildNodeFactory
from .. import models


class ChildNodeRedirectFactory(ChildNodeFactory):
    """Create a NodeRedirect with a target to a Child Node."""
    target = factory.SubFactory(ChildNodeFactory)

    class Meta:
        model = models.NodeRedirect
