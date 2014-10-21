from unittest import mock

from django.http import HttpResponse
from django.test import TestCase

from . import factories
from .. import views


class RouterTest(TestCase):
    """Test that `route_router` correctly deals with the urls handed to it."""
    def test_root(self):
        """route_router delegates to the Root Route's handler for an empty url."""
        url = ''
        factories.RouteFactory.create()
        request = mock.MagicMock()
        handle_path = 'conman.routes.models.Route.handle'
        with mock.patch(handle_path) as handle:
            response = views.route_router(request, url)

        handle.assert_called_with(request, '/' + url)
        self.assertEqual(response, handle(request, '/' + url))

    def test_complex_url(self):
        """route_router finds the url's best match and delegates to its handler."""
        url = 'slug/42/foo/bar/'
        factories.RouteFactory.create()
        request = mock.MagicMock()
        handle_path = 'conman.routes.models.Route.handle'
        with mock.patch(handle_path) as handle:
            response = views.route_router(request, url)

        handle.assert_called_with(request, '/' + url)
        self.assertEqual(response, handle(request, '/' + url))


class RouterIntegrationTest(TestCase):
    """Test that `route_router` is correctly handed urls."""
    def test_root_url(self):
        """The Root Route handler is passed the correct request and root url."""
        url = '/'
        factories.RouteFactory.create()
        handle_path = 'conman.routes.models.Route.handle'
        with mock.patch(handle_path) as handle:
            handle.return_value = HttpResponse()
            response = self.client.get(url)

        handle.assert_called_with(response.wsgi_request, url)

    def test_complex_url(self):
        """The correct request and url is passed through to the route's handler."""
        url = '/slug/42/foo/bar/'
        factories.RouteFactory.create()
        handle_path = 'conman.routes.models.Route.handle'
        with mock.patch(handle_path) as handle:
            handle.return_value = HttpResponse()
            response = self.client.get(url)

        handle.assert_called_with(response.wsgi_request, url)
