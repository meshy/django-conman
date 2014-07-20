from unittest import mock

from django.test import TestCase

from ..handlers import BaseHandler


class BaseHandlerTest(TestCase):
    def test_path(self):
        self.assertEqual(BaseHandler.path(), 'nav_tree.handlers.BaseHandler')

    def test_path_on_subclass(self):
        class TestHandler(BaseHandler):
            __module__ = 'does_not_exist'

        self.assertEqual(TestHandler.path(), 'does_not_exist.TestHandler')


class BaseHandlerInitTest(TestCase):
    def test_init(self):
        node = mock.MagicMock()

        handler = BaseHandler(node)

        self.assertEqual(handler.node, node)
