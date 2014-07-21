from unittest import mock

from django.core.urlresolvers import clear_url_caches, Resolver404
from django.test import TestCase

from ..handlers import BaseHandler, SimpleHandler


class BaseHandlerPathTest(TestCase):
    """Test BaseHandler.path()"""
    def test_path(self):
        """Test directly on base class"""
        self.assertEqual(BaseHandler.path(), 'nav_tree.handlers.BaseHandler')

    def test_path_on_subclass(self):
        """Test on subclass"""
        class TestHandler(BaseHandler):
            __module__ = 'does_not_exist'

        self.assertEqual(TestHandler.path(), 'does_not_exist.TestHandler')


class BaseHandlerInitTest(TestCase):
    """Test BaseHandler.__init__()"""
    def test_init(self):
        """Make sure "node" gets saved on the handler"""
        node = mock.MagicMock()

        handler = BaseHandler(node)

        self.assertEqual(handler.node, node)


class BaseHandlerHandleTest(TestCase):
    """Test BaseHandler.handle()"""
    def setUp(self):
        class TestHandler(BaseHandler):
            urlconf = 'nav_tree.tests.urls'

        self.node = mock.Mock()
        self.request = mock.Mock()
        self.handler = TestHandler(self.node)
        self.view = 'nav_tree.tests.urls.dummy_view'

    def tearDown(self):
        """Stops the tests leaking into each other through the url cache"""
        clear_url_caches()

    def test_handle_basic(self):
        """Show that url resolving works at the root of the urlconf"""
        with mock.patch(self.view) as view:
            response = self.handler.handle(self.request, '/')

        view.assert_called_with(self.request, handler=self.handler)
        self.assertEqual(response, view(self.request, handler=self.handler))

    def test_handle_slug(self):
        """Show that url resolving works with slugs"""
        with mock.patch(self.view) as view:
            response = self.handler.handle(self.request, '/slug/')

        view.assert_called_with(self.request, handler=self.handler, slug='slug')

        expected = view(self.request, handler=self.handler, slug='slug')
        self.assertEqual(response, expected)

    def test_handle_no_url_match(self):
        """Show that an error is thrown when the url does not match"""
        with self.assertRaises(Resolver404):
            with mock.patch(self.view) as view:
                self.handler.handle(self.request, '/no/match/')

        self.assertFalse(view.called)


class SimpleHandlerHandleTest(TestCase):
    """Test SimpleHandler.handle()"""
    def setUp(self):
        class TestHandler(SimpleHandler):
            view = mock.MagicMock()

        self.node = mock.Mock()
        self.request = mock.Mock()
        self.handler = TestHandler(self.node)
        self.view = TestHandler.view

    def tearDown(self):
        """Stops the tests leaking into each other through the url cache"""
        clear_url_caches()

    def test_handle_basic(self):
        """Show that SimpleHandler.view is used ot process the request"""
        response = self.handler.handle(self.request, '/')

        self.view.assert_called_with(self.request, handler=self.handler)
        self.assertEqual(response, self.view(self.request, handler=self.handler))

    def test_handle_slug(self):
        """Show that slugs are not accepted"""
        with self.assertRaises(Resolver404):
            self.handler.handle(self.request, '/slug/')

        self.assertFalse(self.view.called)

    def test_handle_pk(self):
        """Show that pks are not accepted"""
        with self.assertRaises(Resolver404):
            self.handler.handle(self.request, '/42/')

        self.assertFalse(self.view.called)
