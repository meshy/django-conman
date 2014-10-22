from django.test import TestCase

from conman.nav_tree.tests.factories import ChildNodeFactory
from conman.tests.utils import RequestTestCase
from .factories import ChildNodeRedirectFactory
from .. import views


class TestNodeRedirectView(RequestTestCase):
    """Verify behaviour of NodeRedirectView."""
    view = views.NodeRedirectView

    def test_target(self):
        """NodeRedirectView redirects to the target's url."""
        target = ChildNodeFactory.create()
        node = ChildNodeRedirectFactory.create(target=target)
        view = self.get_view()
        response = view(self.create_request(), node=node)

        self.assertEqual(response['Location'], target.url)

    def test_permanent(self):
        """A permanent redirect has status_code 301."""
        node = ChildNodeRedirectFactory.create(permanent=True)
        view = self.get_view()
        response = view(self.create_request(), node=node)

        self.assertEqual(response.status_code, 301)

    def test_temporary(self):
        """A temporary redirect has status_code 302."""
        node = ChildNodeRedirectFactory.create(permanent=False)
        view = self.get_view()
        response = view(self.create_request(), node=node)

        self.assertEqual(response.status_code, 302)


class TestNodeRedirectViewIntegration(TestCase):
    """Check integration of NodeRedirectView."""
    def test_access_redirect(self):
        """Accessing a NodeRedirect's url redirects to its target's url."""
        target = ChildNodeFactory.create()
        node = ChildNodeRedirectFactory.create(target=target)
        response = self.client.get(node.url)

        expected = 'http://testserver' + target.url
        self.assertEqual(response['Location'], expected)
