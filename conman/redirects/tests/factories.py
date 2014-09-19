import factory

from .. import handlers, models
from conman.nav_tree.tests.factories import RootNodeFactory


class NodeRedirectFactory(factory.DjangoModelFactory):
    node = factory.SubFactory(
        RootNodeFactory,
        handler=handlers.NodeRedirectHandler.path(),
    )

    class Meta:
        model = models.NodeRedirect
