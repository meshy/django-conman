from django.core.checks import Error
from django.core.checks.registry import registry
from django.test import SimpleTestCase

from .. import checks


class TestChecks(SimpleTestCase):
    """Test checks for conman pages."""
    def test_registered_checks(self):
        """The correct checks are registered."""
        registered_checks = registry.get_checks()
        self.assertIn(checks.sirtrevor_installed, registered_checks)

    def test_sirtrevor_installed(self):
        """The check passes if django polymorphic is installed."""
        with self.settings(INSTALLED_APPS=['conman.pages', 'sirtrevor']):
            errors = checks.sirtrevor_installed(app_configs=None)

        self.assertEqual(errors, [])

    def test_sirtrevor_not_installed(self):
        """A check fails if django polymorphic is not installed."""
        with self.settings(INSTALLED_APPS=['conman.pages']):
            errors = checks.sirtrevor_installed(app_configs=None)

        error = Error(
            'Django SirTrevor must be in INSTALLED_APPS.',
            hint="Add 'sirtrevor' to INSTALLED_APPS.",
            id='conman.pages.E001',
        )
        self.assertEqual(errors, [error])
