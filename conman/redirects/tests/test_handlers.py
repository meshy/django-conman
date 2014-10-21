from django.test import TestCase

from conman.routes.handlers import SimpleHandler
from ..handlers import RouteRedirectHandler
from ..views import RouteRedirectView


class TestRouteRedirectHandler(TestCase):
    def test_heritage(self):
        """RouteRedirectHandler sublcasses SimpleHandler."""
        self.assertTrue(issubclass(RouteRedirectHandler, SimpleHandler))

    def test_view(self):
        """RouteRedirectHandler uses the RouteRedirectView."""
        view = RouteRedirectHandler.view
        expected = RouteRedirectView.as_view()

        self.assertEqual(view.__name__, expected.__name__)
        self.assertEqual(view.__module__, expected.__module__)
