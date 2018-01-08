import factory

from conman.routes import models


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
            if cls._meta._counter is None:
                cls._meta.next_sequence()
            slug = 'slug{}'.format(cls._meta._counter.seq)
        kwargs['url'] = base + slug + '/'

        return super().create(*args, **kwargs)
