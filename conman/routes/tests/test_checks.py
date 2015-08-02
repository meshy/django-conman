from django.core.checks import Error
from django.core.checks.registry import registry
from django.test import SimpleTestCase

from .. import checks


class TestChecks(SimpleTestCase):
    """Test checks for conman routes."""
    def test_registered_checks(self):
        """The correct checks are registered."""
        registered_checks = registry.get_checks()
        self.assertIn(checks.polymorphic_installed, registered_checks)
        self.assertIn(checks.subclasses_available, registered_checks)

    def test_polymorphic_installed(self):
        """The check passes if django polymorphic is installed."""
        with self.settings(INSTALLED_APPS=['conman.routes', 'polymorphic']):
            errors = checks.polymorphic_installed(app_configs=None)

        self.assertEqual(errors, [])

    def test_polymorphic_not_installed(self):
        """A check fails if django polymorphic is not installed."""
        with self.settings(INSTALLED_APPS=['conman.routes']):
            errors = checks.polymorphic_installed(app_configs=None)

        error = Error(
            'Django Polymorpic must be in INSTALLED_APPS.',
            hint="Add 'polymorphic' to INSTALLED_APPS.",
            id='conman.routes.E001',
        )
        self.assertEqual(errors, [error])

    def test_route_subclasses_exist(self):
        """The check passes if at least one subclass of Route is available."""
        errors = checks.subclasses_available(app_configs=None)

        self.assertEqual(errors, [])
