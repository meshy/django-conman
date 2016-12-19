from unittest import mock

from django.core.urlresolvers import clear_url_caches, Resolver404
from django.db.models import Manager
from django.test import TestCase

from .urls import dummy_view
from ..handlers import BaseHandler, RouteViewHandler, URLConfHandler
from ..models import Route


class BaseHandlerInitTest(TestCase):
    """Test BaseHandler.__init__()."""
    def test_init(self):
        """Make sure "route" gets saved on the handler."""
        route = mock.MagicMock()

        handler = BaseHandler(route)

        self.assertEqual(handler.route, route)


class SubclassHandleTest(TestCase):
    """Test a subclass of BaseHandler's `.handle()` method."""
    def test_not_implemented(self):
        """An error is raised when `handle()` is not implemented."""
        class TestHandler(BaseHandler):
            pass

        msg = 'Subclasses of `BaseHandler` must implement `handle()`.'
        with self.assertRaisesMessage(NotImplementedError, msg):
            # Arguments are unused, so using None here.
            TestHandler(None).handle(None, None)

    def test_implemented(self):
        """No error is raised when `handle()` is implemented."""
        expected = 'a webpage'

        class TestHandler(BaseHandler):
            def handle(self, request, path):
                return expected

        # Arguments are unused, so using None here.
        self.assertEqual(TestHandler(None).handle(None, None), expected)


class URLConfHandlerHandleTest(TestCase):
    """Test URLConfHandler.handle()."""
    def setUp(self):
        """Create a Handler, route, request and view for use in these tests."""
        class URLConfRoute(Route):
            handler_class = URLConfHandler
            urlconf = 'conman.routes.tests.urls'
            base_objects = Manager()

        self.route = URLConfRoute()
        self.request = mock.Mock()
        self.handler = URLConfHandler(self.route)
        self.view = 'conman.routes.tests.urls.dummy_view'

    def tearDown(self):
        """Stop tests leaking into each other through the url cache."""
        clear_url_caches()
        dummy_view.reset_mock()

    def test_handle_basic(self):
        """Show that url resolving works at the root of the urlconf."""
        response = self.handler.handle(self.request, '/')

        dummy_view.assert_called_with(self.request, route=self.route)
        self.assertEqual(response, dummy_view(self.request, route=self.route))

    def test_handle_slug(self):
        """Show that url resolving works with slugs."""
        slug = 'slug'
        response = self.handler.handle(self.request, '/slug/')

        dummy_view.assert_called_with(self.request, route=self.route, slug=slug)

        expected = dummy_view(self.request, route=self.route, slug=slug)
        self.assertEqual(response, expected)

    def test_handle_no_url_match(self):
        """Show that an error is thrown when the url does not match."""
        with self.assertRaises(Resolver404):
            self.handler.handle(self.request, '/no/match/')

        self.assertFalse(dummy_view.called)


class RouteViewHandlerHandleTest(TestCase):
    """Test RouteViewHandler.handle()."""
    def setUp(self):
        """Create a route, request, and view for use in this test."""
        class MockViewRoute(Route):
            view = mock.MagicMock()
            base_objects = Manager()

        self.route = MockViewRoute()
        self.request = mock.Mock()
        self.handler = RouteViewHandler(self.route)
        self.view = MockViewRoute.view

    def tearDown(self):
        """Stop tests leaking into each other through the url cache."""
        clear_url_caches()

    def test_handle_basic(self):
        """Show that Route.view is used to process the request."""
        response = self.handler.handle(self.request, '/')

        self.view.assert_called_with(self.request, route=self.route)
        expected = self.view(self.request, route=self.route)
        self.assertEqual(response, expected)

    def test_handle_slug(self):
        """Show that slugs are not accepted."""
        with self.assertRaises(Resolver404):
            self.handler.handle(self.request, '/slug/')

        self.assertFalse(self.view.called)

    def test_handle_pk(self):
        """Show that pks are not accepted."""
        with self.assertRaises(Resolver404):
            self.handler.handle(self.request, '/42/')

        self.assertFalse(self.view.called)
