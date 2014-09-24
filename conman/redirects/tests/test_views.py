from django.test import TestCase

from .. import views
from .factories import ChildNodeRedirectFactory
from conman.tests.utils import RequestTestCase
from conman.nav_tree.tests.factories import ChildNodeFactory


class TestNodeRedirectView(RequestTestCase):
    def setUp(self):
        self.target = ChildNodeFactory.create()
        self.request = self.create_request()
        self.view = views.NodeRedirectView.as_view()

    def test_permanent(self):
        node = ChildNodeRedirectFactory.create(
            target=self.target,
            permanent=True,
        )
        response = self.view(self.request, node=node)

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], self.target.url)

    def test_temporary(self):
        node = ChildNodeRedirectFactory.create(
            target=self.target,
            permanent=False,
        )
        response = self.view(self.request, node=node)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], self.target.url)


class TestNodeRedirectViewIntegration(TestCase):
    def setUp(self):
        self.target = ChildNodeFactory.create()
        self.expected = 'http://testserver' + self.target.url

    def test_permanent(self):
        node = ChildNodeRedirectFactory.create(
            target=self.target,
            permanent=True,
        )
        response = self.client.get(node.url)

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], self.expected)

    def test_temporary(self):
        node = ChildNodeRedirectFactory.create(
            target=self.target,
            permanent=False,
        )
        response = self.client.get(node.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], self.expected)
