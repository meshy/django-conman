from unittest import mock

from django.test import TestCase
from incuna_test_utils.testcases.urls import URLTestCase

from .. import urls, views


class TestCMSIndexURL(URLTestCase):
    """Make sure that the CMSIndex view has a URL."""
    def test_url(self):
        self.assert_url_matches_view(
            views.CMSIndex,
            '/cms/',
            'cms:index',
        )


class TestCMSURLs(TestCase):
    @mock.patch('conman.cms.urls.url')
    @mock.patch('conman.cms.urls.include')
    @mock.patch('django.apps.apps.get_app_config')
    def test_urls(self, get_app_config, include, url):
        fake_config = mock.Mock()
        fake_config.cms_urls = 'example.path.to.urls'
        fake_config.label = 'example'

        fake_config.managed_apps = {fake_config}
        get_app_config.return_value = fake_config

        cms_urls = list(urls.urls())
        expected = [
            url(r'^$', views.CMSIndex.as_view, name='index'),
            url(r'^example', include(fake_config.cms_urls))
        ]
        self.assertSequenceEqual(cms_urls, expected)
