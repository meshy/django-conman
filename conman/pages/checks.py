from django.apps import apps
from django.core.checks import Error


def sirtrevor_installed(app_configs, **kwargs):
    """Check that Django SirTrevor is installed correctly."""
    errors = []
    try:
        apps.get_app_config('sirtrevor')
    except LookupError:
        error = Error(
            'Django SirTrevor must be in INSTALLED_APPS.',
            hint="Add 'sirtrevor' to INSTALLED_APPS.",
            id='conman.pages.E001',
        )
        errors.append(error)

    return errors
