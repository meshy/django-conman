from .. import handlers, views
from .factories import NodeRedirectFactory
from conman.tests.utils import RequestTestCase
from conman.nav_tree.tests.factories import ChildNodeFactory, RootNodeFactory


class TestNodeRedirectView(RequestTestCase):
    view = views.NodeRedirectView

    def setUp(self):
        self.target = RootNodeFactory.create()
        handler_path = handlers.NodeRedirectHandler.path()
        self.node = ChildNodeFactory(parent=self.target, handler=handler_path)

        self.handler = self.node.get_handler()
        self.request = self.create_request()

    def test_permanent(self):
        NodeRedirectFactory.create(
            target=self.target,
            node=self.node,
            permanent=True,
        )
        response = self.view.as_view()(self.request, handler=self.handler)

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], self.target.url)

    def test_temporary(self):
        NodeRedirectFactory.create(
            target=self.target,
            node=self.node,
            permanent=False,
        )
        response = self.view.as_view()(self.request, handler=self.handler)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], self.target.url)
