from django.test import TestCase

from .. import handlers, views
from conman.nav_tree.handlers import SimpleHandler


class TestPageHandler(TestCase):
    def test_heritage(self):
        self.assertTrue(issubclass(handlers.PageHandler, SimpleHandler))

    def test_view(self):
        view = handlers.PageHandler.view
        expected = views.PageDetail.as_view()

        self.assertEqual(view.__name__, expected.__name__)
        self.assertEqual(view.__module__, expected.__module__)
