import factory

from .. import models


class NodeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Node
