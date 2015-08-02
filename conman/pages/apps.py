from django.apps import AppConfig
from django.core.checks import register

from . import checks


class PageConfig(AppConfig):
    """The AppConfig for conman routes."""
    name = 'conman.pages'

    def ready(self):
        """Register checks for conman routes."""
        register(checks.sirtrevor_installed)
