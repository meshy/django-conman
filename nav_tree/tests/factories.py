import factory

from .. import models


class NodeFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Node
