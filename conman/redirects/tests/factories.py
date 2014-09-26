import factory

from .. import handlers, models
from conman.nav_tree.tests.factories import ChildNodeFactory, RootNodeFactory


class NodeRedirectFactoryMixin(factory.Factory):
    handler = handlers.NodeRedirectHandler.path()

    class Meta:
        model = models.NodeRedirect


class RootNodeRedirectFactory(NodeRedirectFactoryMixin, RootNodeFactory):
    pass


class ChildNodeRedirectFactory(NodeRedirectFactoryMixin, ChildNodeFactory):
    target = factory.SubFactory(ChildNodeFactory)
