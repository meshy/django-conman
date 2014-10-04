import factory

from conman.nav_tree.tests.factories import ChildNodeFactory, RootNodeFactory
from .. import models


class NodeRedirectFactoryMixin(factory.Factory):
    class Meta:
        model = models.NodeRedirect


class RootNodeRedirectFactory(NodeRedirectFactoryMixin, RootNodeFactory):
    pass


class ChildNodeRedirectFactory(NodeRedirectFactoryMixin, ChildNodeFactory):
    target = factory.SubFactory(ChildNodeFactory)
