from conman.routes.tests.factories import RootRouteFactory
from .. import models


class PageFactory(RootRouteFactory):
    """Create instances of Page for testing."""
    class Meta:
        model = models.Page
