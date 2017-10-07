from unittest import mock

from django.contrib import admin
from django.core.checks import Error
from django.core.checks.registry import registry
from django.test import SimpleTestCase

from conman.routes import checks
from tests.models import NestedRouteSubclass


class PolymorphicInstalledTest(SimpleTestCase):
    """Test checks.polymorphic_installed."""
    def test_registered(self):
        """checks.polymorphic_installed is a registered check."""
        registered_checks = registry.get_checks()
        self.assertIn(checks.polymorphic_installed, registered_checks)

    def test_installed(self):
        """The check passes if django polymorphic is installed."""
        with self.settings(INSTALLED_APPS=['conman.routes', 'polymorphic']):
            errors = checks.polymorphic_installed(app_configs=None)

        self.assertEqual(errors, [])

    def test_not_installed(self):
        """The check fails if django polymorphic is not installed."""
        with self.settings(INSTALLED_APPS=['conman.routes']):
            errors = checks.polymorphic_installed(app_configs=None)

        error = Error(
            'Django Polymorpic must be in INSTALLED_APPS.',
            hint="Add 'polymorphic' to INSTALLED_APPS.",
            id='conman.routes.E001',
        )
        self.assertEqual(errors, [error])


class SubclassesAvailableTest(SimpleTestCase):
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


class SubclassesInAdminTest(SimpleTestCase):
    """Test checks.subclasses_in_admin."""
    def test_registered(self):
        """checks.subclasses_in_admin is a registered check."""
        registered_checks = registry.get_checks()
        self.assertIn(checks.subclasses_in_admin, registered_checks)

    def test_in_admin(self):
        """When a Route subclass is in the admin, show no error."""
        errors = checks.subclasses_in_admin(app_configs=None)
        self.assertEqual(errors, [])

    def test_not_in_admin(self):
        """When a Route subclass isn't in the admin, show an error."""
        # Store the registered admin class for teardown.
        admin_class = admin.site._registry[NestedRouteSubclass].__class__
        admin.site.unregister(NestedRouteSubclass)
        try:
            result = checks.subclasses_in_admin(app_configs=None)
        finally:
            # Restore the admin to pre-test status.
            admin.site.register(NestedRouteSubclass, admin_class)

        expected = Error(
            'Route subclasses missing from admin.',
            hint="Missing: {<class 'tests.models.NestedRouteSubclass'>}.",
            id='conman.routes.E003',
        )
        self.assertEqual(result, [expected])

    def test_admin_disabled(self):
        """When the admin isn't active, don't force use of it."""
        admin_class = admin.site._registry[NestedRouteSubclass].__class__

        path = 'conman.routes.checks.apps.is_installed'
        admin.site.unregister(NestedRouteSubclass)
        try:
            with mock.patch(path, return_value=False, autospec=True):
                errors = checks.subclasses_in_admin(app_configs=None)
        finally:
            # Restore the admin to pre-test status.
            admin.site.register(NestedRouteSubclass, admin_class)

        self.assertEqual(errors, [])
