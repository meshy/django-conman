from unittest import mock

from django.http import HttpResponse
from django.test import TestCase

from . import factories
from .. import views


class RouterTest(TestCase):
    """Test that `node_router` correctly deals with the urls handed to it."""
    def test_root(self):
        """node_router delegates to the Root Node's handler for an empty url."""
        url = ''
        factories.NodeFactory.create()
        request = mock.MagicMock()
        handle_path = 'conman.nav_tree.models.Node.handle'
        with mock.patch(handle_path) as handle:
            response = views.node_router(request, url)

        handle.assert_called_with(request, '/' + url)
        self.assertEqual(response, handle(request, '/' + url))

    def test_complex_url(self):
        """node_router finds the url's best match and delegates to its handler."""
        url = 'slug/42/foo/bar/'
        factories.NodeFactory.create()
        request = mock.MagicMock()
        handle_path = 'conman.nav_tree.models.Node.handle'
        with mock.patch(handle_path) as handle:
            response = views.node_router(request, url)

        handle.assert_called_with(request, '/' + url)
        self.assertEqual(response, handle(request, '/' + url))


class RouterIntegrationTest(TestCase):
    """Test that `node_router` is correctly handed urls."""
    def test_root_url(self):
        """The Root Node handler is passed the correct request and root url."""
        url = '/'
        factories.NodeFactory.create()
        handle_path = 'conman.nav_tree.models.Node.handle'
        with mock.patch(handle_path) as handle:
            handle.return_value = HttpResponse()
            response = self.client.get(url)

        handle.assert_called_with(response.wsgi_request, url)

    def test_complex_url(self):
        """The correct request and url is passed through to the node's handler."""
        url = '/slug/42/foo/bar/'
        factories.NodeFactory.create()
        handle_path = 'conman.nav_tree.models.Node.handle'
        with mock.patch(handle_path) as handle:
            handle.return_value = HttpResponse()
            response = self.client.get(url)

        handle.assert_called_with(response.wsgi_request, url)
