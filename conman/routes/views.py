from .models import Route


def route_router(request, url):
    """Catch-all view that delegates view handling to the best Route match."""
    # Django strips the leading / when resolving urls, so we'll just go ahead
    # and add it again. This allows us to use it for resolving later.
    url = '/' + url
    route = Route.objects.best_match_for_path(url)
    return route.handle(request, url)
