from django.test import TestCase

from .. import handlers, views
from conman.nav_tree.handlers import SimpleHandler


class TestPageHandler(TestCase):
    def test_heritage(self):
        self.assertTrue(issubclass(handlers.PageHandler, SimpleHandler))

    def test_view(self):
        self.assertEqual(handlers.PageHandler.view, views.PageDetail)
