from django.apps import apps
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
