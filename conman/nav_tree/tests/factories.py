import factory

from .. import models


class NodeFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Node


class RootNodeFactory(NodeFactory):
    slug = ''
    parent = None


class ChildNodeFactory(NodeFactory):
    parent = factory.SubFactory(RootNodeFactory)
    slug = factory.Sequence('slug{}'.format)
