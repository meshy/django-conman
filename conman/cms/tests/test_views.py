from django.apps import apps
from django.core.urlresolvers import reverse
from django.test import TestCase

from conman.tests.utils import RequestTestCase
from .. import views


class CMSIndexTest(RequestTestCase):
    def test_get(self):
        """CMSIndex returns a 200."""
        view = views.CMSIndex.as_view()

        response = view(self.create_request())

        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        """The CMSIndex view's context contains the managed apps."""
        view = views.CMSIndex()

        context = view.get_context_data()

        expected = apps.get_app_config('cms').managed_apps
        self.assertEqual(context['apps'], expected)


class CMSIndexIntegrationTest(TestCase):
    def test_get(self):
        """CMSIndex uses the correct template."""
        response = self.client.get(reverse('cms:index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms/index.html')
