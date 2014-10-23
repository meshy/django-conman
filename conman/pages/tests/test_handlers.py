from django.test import TestCase

from conman.routes.handlers import SimpleHandler
from .. import handlers, views


class TestPageHandler(TestCase):
    def test_heritage(self):
        """PageHandler subclasses SimpleHandler."""
        self.assertTrue(issubclass(handlers.PageHandler, SimpleHandler))

    def test_view(self):
        """PageHandler uses the PageDetail view."""
        view = handlers.PageHandler.view
        expected = views.PageDetail.as_view()

        self.assertEqual(view.__name__, expected.__name__)
        self.assertEqual(view.__module__, expected.__module__)
