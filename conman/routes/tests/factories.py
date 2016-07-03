import factory

from .. import models


class RouteFactory(factory.DjangoModelFactory):
    """Create instances of Route for testing."""
    url = '/'

    class Meta:
        model = models.Route


class ChildRouteFactory(RouteFactory):
    """Create a Route with a url dependent on a slug or parent."""
    @classmethod
    def create(cls, *args, parent=None, slug=None, **kwargs):
        """Calculate a url based on a slug or parent."""
        assert 'url' not in kwargs

        base = '/' if parent is None else parent.url
        if slug is None:
            slug = 'slug{}'.format(cls._counter.seq)
        kwargs['url'] = base + slug + '/'

        return super().create(*args, **kwargs)
