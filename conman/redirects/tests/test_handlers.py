from django.test import TestCase

from conman.nav_tree.handlers import SimpleHandler
from ..handlers import NodeRedirectHandler
from ..views import NodeRedirectView


class TestNodeRedirectHandler(TestCase):
    """Test the NodeRedirectHandler."""
    def test_heritage(self):
        """NodeRedirectHandler sublcasses SimpleHandler."""
        self.assertTrue(issubclass(NodeRedirectHandler, SimpleHandler))

    def test_view(self):
        """NodeRedirectHandler uses the NodeRedirectView."""
        view = NodeRedirectHandler.view
        expected = NodeRedirectView.as_view()

        self.assertEqual(view.__name__, expected.__name__)
        self.assertEqual(view.__module__, expected.__module__)
