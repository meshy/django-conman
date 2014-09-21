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
