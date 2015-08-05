from unittest import mock

from django.core.checks import Error
from django.core.checks.registry import registry
from django.test import SimpleTestCase

from .. import checks


class TestPolymorphicInstalled(SimpleTestCase):
    """Test checks.polymorphic_installed."""
    check = staticmethod(checks.polymorphic_installed)

    def test_registered(self):
        """checks.polymorphic_installed is a registered check."""
        registered_checks = registry.get_checks()
        self.assertIn(self.check, registered_checks)

    def test_installed(self):
        """The check passes if django-polymorphic is installed."""
        with self.settings(INSTALLED_APPS=['conman.routes', 'polymorphic']):
            errors = self.check(app_configs=None)

        self.assertEqual(errors, [])

    def test_not_installed(self):
        """The check fails if django-polymorphic is not installed."""
        with self.settings(INSTALLED_APPS=['conman.routes']):
            errors = self.check(app_configs=None)

        error = Error(
            'Django Polymorpic must be in INSTALLED_APPS.',
            hint="Add 'polymorphic' to INSTALLED_APPS.",
            id='conman.routes.E001',
        )
        self.assertEqual(errors, [error])


class TestPolymorphicTreeInstalled(SimpleTestCase):
    """Test checks.polymorphic_tree_installed."""
    check = staticmethod(checks.polymorphic_tree_installed)

    def test_registered(self):
        """checks.polymorphic_tree_installed is a registered check."""
        registered_checks = registry.get_checks()
        self.assertIn(self.check, registered_checks)

    def test_installed(self):
        """The check passes if django-polymorphic-tree is installed."""
        with self.settings(INSTALLED_APPS=['conman.routes', 'polymorphic_tree']):
            errors = self.check(app_configs=None)

        self.assertEqual(errors, [])

    def test_not_installed(self):
        """The check fails if django polymorphic is not installed."""
        with self.settings(INSTALLED_APPS=['conman.routes']):
            errors = self.check(app_configs=None)

        error = Error(
            'Django Polymorpic Tree must be in INSTALLED_APPS.',
            hint="Add 'polymorphic_tree' to INSTALLED_APPS.",
            id='conman.routes.E003',
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
