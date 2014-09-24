from unittest import mock

from django.core.urlresolvers import clear_url_caches, Resolver404
from django.test import TestCase
from django.views.generic import View

from ..handlers import BaseHandler, SimpleHandler


class BaseHandlerPathTest(TestCase):
    """Test BaseHandler.path()"""
    def test_path(self):
        """Test directly on base class"""
        base_handler_path = 'conman.nav_tree.handlers.base.BaseHandler'
        self.assertEqual(BaseHandler.path(), base_handler_path)

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
            urlconf = 'conman.nav_tree.tests.urls'

        self.node = mock.Mock()
        self.request = mock.Mock()
        self.handler = TestHandler(self.node)
        self.view = 'conman.nav_tree.tests.urls.dummy_view'

    def tearDown(self):
        """Stops the tests leaking into each other through the url cache"""
        clear_url_caches()

    def test_handle_basic(self):
        """Show that url resolving works at the root of the urlconf"""
        with mock.patch(self.view) as view:
            response = self.handler.handle(self.request, '/')

        view.assert_called_with(self.request, node=self.node)
        self.assertEqual(response, view(self.request, node=self.node))

    def test_handle_slug(self):
        """Show that url resolving works with slugs"""
        slug = 'slug'
        with mock.patch(self.view) as view:
            response = self.handler.handle(self.request, '/slug/')

        view.assert_called_with(self.request, node=self.node, slug=slug)

        expected = view(self.request, node=self.node, slug=slug)
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
        self.node.get_handler.return_value = self.handler
        self.view = TestHandler.view

    def tearDown(self):
        """Stops the tests leaking into each other through the url cache"""
        clear_url_caches()

    def test_handle_basic(self):
        """Show that SimpleHandler.view is used to process the request"""
        response = self.handler.handle(self.request, '/')

        self.view.assert_called_with(self.request, node=self.node)
        expected = self.view(self.request, node=self.node)
        self.assertEqual(response, expected)

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


class SimpleHandlerViewBindingTest(TestCase):
    """Views should not unexpectedly "bind" to SimpleHandler subclasses"""
    def test_unbound_function(self):
        """Make sure that the handler is not bound to self on the view"""
        def unbound_function(request, **kwargs):
            return request

        class TestHandler(SimpleHandler):
            view = unbound_function

        handler = TestHandler(None)  # First arg here not used
        request = mock.Mock()
        response = handler.view(request)
        self.assertIs(response, request)

    def test_bound_function(self):
        """Make sure that class based views get the expected args"""
        class TestView(View):
            def dispatch(self, request, node=None):
                return self, request

        class TestHandler(SimpleHandler):
            view = TestView.as_view()

        handler = TestHandler(None)  # First arg here not used
        request = mock.Mock()
        self_arg, request_arg = handler.view(request)
        self.assertIsInstance(self_arg, TestView)
        self.assertIs(request_arg, request)
