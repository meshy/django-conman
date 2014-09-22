from django.test import TestCase

from .. import views
from . import factories
from conman.tests.utils import RequestTestCase


class TestPageDetail(RequestTestCase):
    def test_get_object(self):
        request = self.create_request()
        page = factories.PageFactory.create()
        handler = page.get_handler()

        view = views.PageDetail(request=request, kwargs={'handler': handler})
        obj = view.get_object()

        self.assertEqual(obj, page)


class TestPageDetailIntegration(TestCase):
    view = views.PageDetail

    def test_get(self):
        page = factories.PageFactory.create(content='This is a test')
        response = self.client.get(page.url)
        self.assertIn(page.content, response.rendered_content)
