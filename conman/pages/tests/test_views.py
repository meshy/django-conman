from conman.tests.utils import RequestTestCase
from . import factories
from .. import views


class TestPageDetail(RequestTestCase):
    """Test the PageDetail view."""
    def test_get_object(self):
        """PageDetail displays the page instance passed in the route kwarg."""
        request = self.create_request()
        page = factories.PageFactory.create()

        view = views.PageDetail(request=request, kwargs={'route': page})
        obj = view.get_object()

        self.assertEqual(obj, page)

    def test_integration_get(self):
        """A page's content is rendered at its url."""
        page = factories.PageFactory.create(content='This is a test')
        response = self.client.get(page.url)
        self.assertIn(page.content, response.rendered_content)
