from django.core.urlresolvers import resolve, Resolver404
from django.test import TestCase

from .. import views


class TestNavTreeURLRouter(TestCase):
    def assert_url_uses_router(self, url):
        resolved_view = resolve(url)
        expected_view = views.node_router
        self.assertEqual(resolved_view.func, expected_view)

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
        self.assert_url_uses_router('/')

    def test_child_url(self):
        self.assert_url_uses_router('/slug/')

    def test_nested_child_url(self):
        self.assert_url_uses_router('/foo/bar/')

    def test_numerical_url(self):
        self.assert_url_uses_router('/meanings/42/')

    def test_without_trailing_slash(self):
        with self.assertRaises(Resolver404):
            self.assert_url_uses_router('/fail')
