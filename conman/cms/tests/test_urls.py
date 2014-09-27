from incuna_test_utils.testcases.urls import URLTestCase

from .. import views


class TestCMSIndexURL(URLTestCase):
    """Make sure that the CMSIndex view has a URL"""
    def test_url(self):
        self.assert_url_matches_view(
            views.CMSIndex,
            '/cms/',
            'cms-index',
        )
