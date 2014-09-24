from django.core.urlresolvers import resolve


class BaseHandler:
    """
    Abstract base class for `Node` handlers.

    Subclasses should define a `urlconf` property as a dotted path. This will
    be used to resolve a view when handling requests.

    Views referenced in the `urlconf` will receive `node` as a kwarg, as
    well as the other args and kwargs they would expect given their urlpattern.
    """
    @classmethod
    def path(cls):
        """Get dotted-path of this class"""
        return '{}.{}'.format(cls.__module__, cls.__name__)

    def __init__(self, node):
        """Store the Node so that we know what we're handling."""
        self.node = node

    def handle(self, request, path):
        """
        Resolve `path` to a view, and get it to handle the `request`.

        Returns the `HttpResponse` returned by the view.

        Raises `django.core.urlresolvers.Resolver404` if `path` isn't found.
        """
        view, args, kwargs = resolve(path, urlconf=self.urlconf)
        return view(request, *args, node=self.node, **kwargs)
