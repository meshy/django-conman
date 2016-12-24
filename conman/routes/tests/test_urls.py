from django.core.urlresolvers import resolve, Resolver404
from django.test import TestCase

from .. import views


class NavTreeURLRouterTest(TestCase):
    """Test the route_router view."""
    def assert_url_uses_router(self, url):
        """Check a url resolves to the route_router view."""
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func, views.route_router)

    def test_blank_url(self):
        """Blank urls should not resolve.

        This is actually a test of django, as urls must start with `/`.
        """
        with self.assertRaises(Resolver404):
            self.assert_url_uses_router('')

    def test_double_slash_url(self):
        """Trailing slashes should trail something."""
        with self.assertRaises(Resolver404):
            self.assert_url_uses_router('//')

    def test_root_url(self):
        """The root url is resolved using views.route_router."""
        self.assert_url_uses_router('/')

    def test_child_url(self):
        """A child url is resolved using views.route_router."""
        self.assert_url_uses_router('/slug/')

    def test_nested_child_url(self):
        """A nested child url is resolved using views.route_router."""
        self.assert_url_uses_router('/foo/bar/')

    def test_numerical_url(self):
        """A numeric url is resolved using views.route_router."""
        self.assert_url_uses_router('/meanings/42/')

    def test_without_trailing_slash(self):
        """A url without a trailing slash is not resolved by views.route_router."""
        with self.assertRaises(Resolver404):
            self.assert_url_uses_router('/fail')
