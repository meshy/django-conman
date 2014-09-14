from .. import views
from . import factories
from conman.tests.utils import RequestTestCase


class TestPageDetail(RequestTestCase):
    view = views.PageDetail

    def test_get_context_data(self):
        request = self.create_request()
        page = factories.PageFactory.create()
        node = page.node
        handler = node.get_handler_class()(page.node)

        view = self.view(request=request, kwargs={'handler': handler})
        context = view.get_context_data()

        expected = {
            'page': page,
            'node': node,
            'handler': handler,
            'view': view,
        }
        self.assertEqual(context, expected)
