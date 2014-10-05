from django.test import TestCase

from conman.nav_tree.handlers import SimpleHandler
from .. import handlers, views


class TestPageHandler(TestCase):
    def test_heritage(self):
        self.assertTrue(issubclass(handlers.PageHandler, SimpleHandler))

    def test_view(self):
        view = handlers.PageHandler.view
        expected = views.PageDetail.as_view()

        self.assertEqual(view.__name__, expected.__name__)
        self.assertEqual(view.__module__, expected.__module__)
