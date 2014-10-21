from conman.routes.tests.factories import RootNodeFactory
from .. import models


class PageFactory(RootNodeFactory):
    """Create instances of Page for testing."""
    class Meta:
        model = models.Page
