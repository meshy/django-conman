from django.apps import AppConfig
from django.core.checks import register

from . import checks


class RouteConfig(AppConfig):
    """The AppConfig for conman routes."""
    name = 'conman.routes'

    def ready(self):
        """Register checks for conman routes."""
        register(checks.polymorphic_installed)
        register(checks.subclasses_available)
        register(checks.subclasses_in_admin)
