from django.db import models

from conman.routes.handlers import TemplateHandler, URLConfHandler
from conman.routes.managers import RouteManager
from conman.routes.models import Route


class RouteSubclass(Route):
    """A Route for testing direct subclasses of Route."""
    # Silence RemovedInDjango20Warning about manager inheritance.
    objects = RouteManager()

    @staticmethod
    def view(request, route):
        """A dummy view to keep the checks happy."""
        return ''


class NestedRouteSubclass(RouteSubclass):
    """A Route for testing nested subclasses of Route."""
    # Silence RemovedInDjango20Warning about manager inheritance.
    objects = RouteManager()


class TemplateRoute(Route):
    """A Route for testing TemplateHandler."""
    content = models.TextField()
    handler_class = TemplateHandler
    template_name = 'basic_template.html'
    # Silence RemovedInDjango20Warning about manager inheritance.
    objects = RouteManager()


class URLConfRoute(Route):
    """A Route for testing URLConfHandler."""
    handler_class = URLConfHandler
    urlconf = 'tests.routes.urls'
    # Silence RemovedInDjango20Warning about manager inheritance.
    objects = RouteManager()
