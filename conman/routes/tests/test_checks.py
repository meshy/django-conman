from unittest import mock

from django.core.checks import Error
from django.core.checks.registry import registry
from django.test import SimpleTestCase

from .. import checks


class TestRequirementsInstalled(SimpleTestCase):
    """Test checks.requirements_installed."""
    def setUp(self):
        self.installed = [
            'conman.routes',
            'polymorphic',
            'django.contrib.sites',
        ]

    def test_registered(self):
        """checks.requirements_installed is a registered check."""
        registered_checks = registry.get_checks()
        self.assertIn(checks.requirements_installed, registered_checks)

    def test_installed(self):
        """The check passes if all requirements are installed."""
        with self.settings(INSTALLED_APPS=self.installed):
            errors = checks.requirements_installed(app_configs=None)

        self.assertEqual(errors, [])

    def test_polymorphic_not_installed(self):
        """The check fails if django polymorphic is not installed."""
        self.installed.remove('polymorphic')
        with self.settings(INSTALLED_APPS=self.installed):
            errors = checks.requirements_installed(app_configs=None)

        error = Error(
            'Missing requirements must be installed.',
            hint='Add polymorphic to INSTALLED_APPS.',
            id='conman.routes.E001',
        )
        self.assertEqual(errors, [error])

    def test_sites_not_installed(self):
        """The check fails if django sites are not installed."""
        self.installed.remove('django.contrib.sites')
        with self.settings(INSTALLED_APPS=self.installed):
            errors = checks.requirements_installed(app_configs=None)

        error = Error(
            'Missing requirements must be installed.',
            hint='Add django.contrib.sites to INSTALLED_APPS.',
            id='conman.routes.E001',
        )
        self.assertEqual(errors, [error])

    def test_multiple_not_installed(self):
        """The check fails if multiple requirements are not installed."""
        self.installed.remove('django.contrib.sites')
        self.installed.remove('polymorphic')
        with self.settings(INSTALLED_APPS=self.installed):
            errors = checks.requirements_installed(app_configs=None)

        error = Error(
            'Missing requirements must be installed.',
            hint='Add django.contrib.sites, polymorphic to INSTALLED_APPS.',
            id='conman.routes.E001',
        )
        self.assertEqual(errors, [error])


class TestSubclassesAvailable(SimpleTestCase):
    """Test checks.subclasses_available."""
    def test_registered(self):
        """checks.subclasses_available is a registered check."""
        registered_checks = registry.get_checks()
        self.assertIn(checks.subclasses_available, registered_checks)

    def test_available(self):
        """The check passes if at least one subclass of Route is available."""
        errors = checks.subclasses_available(app_configs=None)

        self.assertEqual(errors, [])

    def test_unavailable(self):
        """The check fails if no subclass of Route is available."""
        with mock.patch('conman.routes.models.Route.__subclasses__') as subclasses:
            subclasses.return_value = []
            errors = checks.subclasses_available(app_configs=None)

        error = Error(
            'No Route subclasses are available.',
            hint='Add another conman module to INSTALLED_APPS.',
            id='conman.routes.E002',
        )
        self.assertEqual(errors, [error])
