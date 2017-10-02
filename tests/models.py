from conman.routes.models import Route
from conman.routes.managers import RouteManager


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
