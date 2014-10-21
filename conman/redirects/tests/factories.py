import factory

from conman.routes.tests.factories import ChildRouteFactory
from .. import models


class ChildRouteRedirectFactory(ChildRouteFactory):
    """Create a RouteRedirect with a target to a Child Route."""
    target = factory.SubFactory(ChildRouteFactory)

    class Meta:
        model = models.RouteRedirect
