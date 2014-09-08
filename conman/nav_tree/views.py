from .models import Node


def node_router(request, url):
    """Catch-all view that delegates view handling to the best Node match."""
    # Django strips the leading / when resolving urls, so we'll just go ahead
    # and add it again. This allows us to use it for resolving later.
    url = '/' + url
    node = Node.objects.best_match_for_path(url)
    return node.handle(request, url)
