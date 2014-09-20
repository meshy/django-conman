from .. import views
from . import factories
from conman.tests.utils import IntegrationTestCase, RequestTestCase


class TestPageDetail(RequestTestCase):
    def test_get_object(self):
        request = self.create_request()
        page = factories.PageFactory.create()
        handler = page.node_ptr.get_handler()

        view = views.PageDetail(request=request, kwargs={'handler': handler})
        obj = view.get_object()

        self.assertEqual(obj, page)


class TestPageDetailIntegration(IntegrationTestCase):
    view = views.PageDetail

    def test_get(self):
        page = factories.PageFactory.create(content='This is a test')
        handler = page.node_ptr.get_handler()
        response = self.access_view_and_render_response(handler=handler)
        self.assert_count(page.content, response, 1)
