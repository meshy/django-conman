from django.apps import apps
from django.contrib import admin
from django.core.checks import Error


def polymorphic_installed(app_configs, **kwargs):
    """Check that Django Polymorphic is installed correctly."""
    errors = []
    try:
        apps.get_app_config('polymorphic')
    except LookupError:
        error = Error(
            'Django Polymorpic must be in INSTALLED_APPS.',
            hint="Add 'polymorphic' to INSTALLED_APPS.",
            id='conman.routes.E001',
        )
        errors.append(error)

    return errors


def subclasses_available(app_configs, **kwargs):
    """Check that at least one Route subclass is available."""
    errors = []
    routes = apps.get_app_config('routes')
    Route = routes.get_model('Route')
    if not Route.__subclasses__():
        error = Error(
            'No Route subclasses are available.',
            hint='Add another conman module to INSTALLED_APPS.',
            id='conman.routes.E002',
        )
        errors.append(error)

    return errors


def subclasses_in_admin(app_configs, **kwargs):
    """Catch Route subclasses that are not registered in the admin."""
    if not apps.is_installed('django.contrib.admin'):
        return []

    Route = apps.get_model('routes.Route')
    route_subclasses = set(Route.get_subclasses())
    missing = route_subclasses.difference(admin.site._registry)
    if missing:
        return [Error(
            'Route subclasses missing from admin.',
            hint='Missing: {}.'.format(missing),
            id='conman.routes.E003',
        )]
    return []
