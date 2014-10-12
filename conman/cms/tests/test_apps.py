from unittest import mock

from django.apps import apps
from django.test import TestCase


class CMSAppRegistrationTest(TestCase):
    """Test the app registration process."""
    def setUp(self):
        """
        Make the cms app available to all tests.

        Store the original managed apps registry to allow a test to edit it.
        """
        self.config = apps.get_app_config('cms')

        self._original_registry = self.config.managed_apps

    def tearDown(self):
        """Restore the managed apps registry to the cms app config."""
        self.config._managed_apps = self._original_registry

    def test_apps_can_register(self):
        """An app can be registered if it has the cms_urls attribute."""
        mock_app = mock.Mock(spec=self.config)
        mock_app.cms_urls = 'has.been.set'

        self.config.manage_app(mock_app)

        self.assertIn(mock_app, self.config.managed_apps)

    def test_app_needs_cms_urls(self):
        """An app without the cms_urls attribute cannot be registered."""
        mock_app = mock.Mock(spec=self.config)

        with self.assertRaises(ValueError):
            self.config.manage_app(mock_app)
