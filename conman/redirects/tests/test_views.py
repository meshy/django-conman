from django.test import TestCase

from conman.routes.tests.factories import ChildRouteFactory
from conman.tests.utils import RequestTestCase
from .factories import ChildRouteRedirectFactory
from .. import views


class TestRouteRedirectView(RequestTestCase):
    """Verify behaviour of RouteRedirectView."""
    def setUp(self):
        self.target = ChildRouteFactory.create()
        self.request = self.create_request()
        self.view = views.RouteRedirectView.as_view()

    def test_target(self):
        """RouteRedirectView redirects to the target's url."""
        route = ChildRouteRedirectFactory.create(target=self.target)
        response = self.view(self.request, route=route)

        self.assertEqual(response['Location'], self.target.url)

    def test_permanent(self):
        """A permanent redirect has status_code 301."""
        route = ChildRouteRedirectFactory.create(permanent=True)
        response = self.view(self.request, route=route)

        self.assertEqual(response.status_code, 301)

    def test_temporary(self):
        """A temporary redirect has status_code 302."""
        route = ChildRouteRedirectFactory.create(permanent=False)
        response = self.view(self.request, route=route)

        self.assertEqual(response.status_code, 302)


class TestRouteRedirectViewIntegration(TestCase):
    """Check integration of RouteRedirectView."""
    def setUp(self):
        self.target = ChildRouteFactory.create()
        self.expected = 'http://testserver' + self.target.url

    def test_access_redirect(self):
        """Accessing a RouteRedirect's url redirects to its target's url."""
        route = ChildRouteRedirectFactory.create(target=self.target)
        response = self.client.get(route.url)

        self.assertEqual(response['Location'], self.expected)
