from django.apps import apps
from django.core.checks import Error


def requirements_installed(app_configs, **kwargs):
    """Check that requirements are installed correctly."""
    missing_apps = []
    required_apps = [
        'django.contrib.sites',
        'polymorphic',
    ]

    for app in required_apps:
        if not apps.is_installed(app):
            missing_apps.append(app)

    if not missing_apps:
        return []

    return [Error(
        'Missing requirements must be installed.',
        hint='Add {} to INSTALLED_APPS.'.format(', '.join(missing_apps)),
        id='conman.routes.E001',
    )]


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
