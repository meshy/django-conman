from conman.routes.tests.factories import RouteFactory
from .. import models


class PageFactory(RouteFactory):
    """Create instances of Page for testing."""
    class Meta:
        model = models.Page
