import factory

from conman.routes.tests.factories import ChildRouteFactory, RouteFactory
from .. import models


class ChildRouteRedirectFactory(ChildRouteFactory):
    """Create a RouteRedirect with a target to a Child Route."""
    target = factory.SubFactory(ChildRouteFactory)

    class Meta:
        model = models.RouteRedirect


class URLRedirectFactory(RouteFactory):
    """Create a URLRedirect with a target url."""
    target = factory.Sequence('https://example.com/{}'.format)

    class Meta:
        model = models.URLRedirect
