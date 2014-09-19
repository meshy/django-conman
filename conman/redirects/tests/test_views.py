from .. import handlers, views
from .factories import NodeRedirectFactory
from conman.tests.utils import IntegrationTestCase, RequestTestCase
from conman.nav_tree.tests.factories import ChildNodeFactory, RootNodeFactory


class TestNodeRedirectView(RequestTestCase):
    view = views.NodeRedirectView

    def test_get(self):
        request = self.create_request()
        target = RootNodeFactory.create()
        handler_path = handlers.NodeRedirectHandler.path()
        node = ChildNodeFactory(parent=target, handler=handler_path)
        node_redirect = NodeRedirectFactory.create(target=target, node=node)
        handler = node_redirect.node.get_handler()

        response = self.view.as_view()(request, handler=handler)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], target.url)
