from django.test import TestCase

from conman.tests.utils import RequestTestCase
from conman.url_tree.tests.factories import ChildNodeFactory
from .factories import ChildNodeRedirectFactory
from .. import views


class TestNodeRedirectView(RequestTestCase):
    def setUp(self):
        self.target = ChildNodeFactory.create()
        self.request = self.create_request()
        self.view = views.NodeRedirectView.as_view()

    def test_target(self):
        """NodeRedirectView redirects to the target's url."""
        node = ChildNodeRedirectFactory.create(target=self.target)
        response = self.view(self.request, node=node)

        self.assertEqual(response['Location'], self.target.url)

    def test_permanent(self):
        """A permanent redirect has status_code 301."""
        node = ChildNodeRedirectFactory.create(permanent=True)
        response = self.view(self.request, node=node)

        self.assertEqual(response.status_code, 301)

    def test_temporary(self):
        """A temporary redirect has status_code 302."""
        node = ChildNodeRedirectFactory.create(permanent=False)
        response = self.view(self.request, node=node)

        self.assertEqual(response.status_code, 302)


class TestNodeRedirectViewIntegration(TestCase):
    def setUp(self):
        self.target = ChildNodeFactory.create()
        self.expected = 'http://testserver' + self.target.url

    def test_access_redirect(self):
        """Accessing a NodeRedirect's url redirects to its target's url."""
        node = ChildNodeRedirectFactory.create(target=self.target)
        response = self.client.get(node.url)

        self.assertEqual(response['Location'], self.expected)
