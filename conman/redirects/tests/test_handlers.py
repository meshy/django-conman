from django.test import TestCase

from ..handlers import NodeRedirectHandler
from ..views import NodeRedirectView
from conman.nav_tree.handlers import SimpleHandler


class TestNodeRedirectHandler(TestCase):
    def test_heritage(self):
        self.assertTrue(issubclass(NodeRedirectHandler, SimpleHandler))

    def test_view(self):
        view = NodeRedirectHandler.view
        expected = NodeRedirectView.as_view()

        self.assertEqual(view.__name__, expected.__name__)
        self.assertEqual(view.__module__, expected.__module__)
