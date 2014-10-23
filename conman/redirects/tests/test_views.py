from django.test import TestCase

from conman.routes.tests.factories import ChildRouteFactory
from conman.tests.utils import RequestTestCase
from .factories import ChildRouteRedirectFactory
from .. import views


class TestRouteRedirectView(RequestTestCase):
    """Verify behaviour of RouteRedirectView."""
    view = views.RouteRedirectView

    def test_target(self):
        """RouteRedirectView redirects to the target's url."""
        target = ChildRouteFactory.create()
        route = ChildRouteRedirectFactory.create(target=target)
        view = self.get_view()
        response = view(self.create_request(), route=route)

        self.assertEqual(response['Location'], target.url)

    def test_permanent(self):
        """A permanent redirect has status_code 301."""
        route = ChildRouteRedirectFactory.create(permanent=True)
        view = self.get_view()
        response = view(self.create_request(), route=route)

        self.assertEqual(response.status_code, 301)

    def test_temporary(self):
        """A temporary redirect has status_code 302."""
        route = ChildRouteRedirectFactory.create(permanent=False)
        view = self.get_view()
        response = view(self.create_request(), route=route)

        self.assertEqual(response.status_code, 302)


class TestRouteRedirectViewIntegration(TestCase):
    """Check integration of RouteRedirectView."""
    def test_access_redirect(self):
        """Accessing a RouteRedirect's url redirects to its target's url."""
        target = ChildRouteFactory.create()
        route = ChildRouteRedirectFactory.create(target=target)
        response = self.client.get(route.url)

        expected = 'http://testserver' + target.url
        self.assertEqual(response['Location'], expected)
