from django.test import TestCase

from .. import views
from .factories import ChildNodeRedirectFactory
from conman.tests.utils import RequestTestCase
from conman.nav_tree.tests.factories import RootNodeFactory


class TestNodeRedirectView(RequestTestCase):
    def setUp(self):
        self.root = RootNodeFactory.create()
        self.request = self.create_request()
        self.view = views.NodeRedirectView.as_view()

    def test_permanent(self):
        node = ChildNodeRedirectFactory.create(
            parent=self.root,
            target=self.root,
            permanent=True,
        )
        handler = node.node_ptr.get_handler()
        response = self.view(self.request, handler=handler)

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], self.root.url)

    def test_temporary(self):
        node = ChildNodeRedirectFactory.create(
            parent=self.root,
            target=self.root,
            permanent=False,
        )
        handler = node.node_ptr.get_handler()
        response = self.view(self.request, handler=handler)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], self.root.url)


class TestNodeRedirectViewIntegration(TestCase):
    def setUp(self):
        self.root = RootNodeFactory.create()

    def test_permanent(self):
        node = ChildNodeRedirectFactory.create(
            parent=self.root,
            target=self.root,
            permanent=True,
        )
        response = self.client.get(node.url)

        self.assertEqual(response.status_code, 301)
        expected = 'http://testserver' + self.root.url
        self.assertEqual(response['Location'], expected)

    def test_temporary(self):
        node = ChildNodeRedirectFactory.create(
            parent=self.root,
            target=self.root,
            permanent=False,
        )
        response = self.client.get(node.url)

        self.assertEqual(response.status_code, 302)
        expected = 'http://testserver' + self.root.url
        self.assertEqual(response['Location'], expected)
