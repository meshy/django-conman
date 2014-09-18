from django.test import TestCase

from ..handlers import NodeRedirectHandler
from ..views import NodeRedirectView
from conman.nav_tree.handlers import SimpleHandler


class TestNodeRedirectHandler(TestCase):
    def test_heritage(self):
        self.assertTrue(issubclass(NodeRedirectHandler, SimpleHandler))

    def test_view(self):
        self.assertEqual(NodeRedirectHandler.view, NodeRedirectView)
