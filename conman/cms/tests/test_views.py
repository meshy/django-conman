from conman.tests.utils import RequestTestCase
from django.core.urlresolvers import reverse
from django.test import TestCase

from .. import views


class CMSIndexTest(RequestTestCase):
    def test_get(self):
        """Can CMSIndex return a 200?"""
        view = views.CMSIndex.as_view()

        response = view(self.create_request())

        self.assertEqual(response.status_code, 200)



class CMSIndexIntegrationTest(TestCase):
    def test_get(self):
        """Does CMSIndex use the correct template?"""
        response = self.client.get(reverse('cms-index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cms/index.html')
