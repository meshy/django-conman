from django.test import TestCase

from conman.tests.utils import RequestTestCase
from . import factories
from .. import views


class TestPageDetail(RequestTestCase):
    """Unit test PageDetail."""
    def test_get_object(self):
        """PageDetail displays the page instance passed in the node kwarg."""
        request = self.create_request()
        page = factories.PageFactory.create()

        view = views.PageDetail(request=request, kwargs={'node': page})
        obj = view.get_object()

        self.assertEqual(obj, page)


class TestPageDetailIntegration(TestCase):
    def test_get(self):
        """A page's content is rendered at its url."""
        page = factories.PageFactory.create(content='This is a test')
        response = self.client.get(page.url)
        self.assertIn(page.content, response.rendered_content)
